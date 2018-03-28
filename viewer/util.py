import datetime
import os
import platform
import pytz
import re
import time

from django.conf import settings
from .models import Entry


MARKDOWN_LOCATION = '/Users/daniel/diary/entries'


def unix_time_to_local_datetime(unix_time):
    local_tz = pytz.timezone(settings.TIME_ZONE)
    utc_dt = datetime.datetime.utcfromtimestamp(unix_time).replace(tzinfo=pytz.utc)
    local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))
    return local_dt


def creation_date(path_to_file):
    '''
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    Returns a datetime.
    '''
    if platform.system() == 'Windows':
        ut = os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            ut = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            ut = stat.st_mtime
    return unix_time_to_local_datetime(ut)


def get_unix_time_from_text(body):
    original_unix_time = 0
    for line in body.splitlines():
        try:
            original_unix_time = int(
                re.match(r'^Unix time at noon: (\d+)$', line)[1]
            )
        except TypeError:
            original_unix_time = 0
        if original_unix_time != 0:
            return original_unix_time
    return original_unix_time


def get_entry_from_file(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        title = os.path.basename(os.path.normpath(fname))
        title = '.'.join(title.split('.')[:-1])
        try:
            # All this date stuff is a bit messy.
            date = datetime.datetime.strptime(title, '%Y-%m-%d')
            ut = time.mktime(date.timetuple())
            date = unix_time_to_local_datetime(ut)
        except ValueError:
            date = creation_date(fname)
            print('WARNING: Couldn\'t get date from the file name: ' + fname)
        modified = unix_time_to_local_datetime(os.path.getmtime(fname))
        body = f.read()
        original_unix_time = get_unix_time_from_text(body)
        e = Entry(
            title=title,
            fname=fname,
            date=date,
            modified=modified,
            body=body,
            original_unix_time=original_unix_time,
        )
        return e


def load_all_markdown():
    for i in os.listdir(MARKDOWN_LOCATION):
        if os.path.splitext(i)[-1] != '.md':
            continue
        e = get_entry_from_file(os.path.join(MARKDOWN_LOCATION, i))
        e.save()
