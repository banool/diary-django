from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Entry, START
from .util import get_entry_from_file

import logging
import os
import re
import subprocess
import tempfile
import time

logger = logging.getLogger(__name__)

DATE_RE = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$'


def index(request):
    entries = Entry.objects.order_by('-date')
    regular = [
        e for e in entries if re.match(DATE_RE, e.title)
    ]
    other = [
        e for e in entries if not re.match(DATE_RE, e.title)
    ]
    recent = [e for e in regular if e.date_text() >= START]
    historical = [e for e in regular if e.date_text() < START]
    context = {
        'entries': recent,
        'others': other,
        'historical': historical,
    }
    return render(request, 'diary/index.html', context)


def entry(request, year, month, day):
    entries = Entry.objects.filter(
        date__year=year, date__month=month, date__day=day,
    )
    if len(entries) == 0:
        raise Http404('Diary entry does not exist :(')
    if len(entries) > 1:
        return HttpResponse('There is more than one entry???')
    entry = entries[0]
    # Check that the entry hasn't been modified since it was last read in to
    # the database.
    curr_modified = time.mktime(entry.modified.timetuple())
    new_modified = int(os.path.getmtime(entry.fname))
    if new_modified > curr_modified:
        new_entry = get_entry_from_file(entry.fname)
        entry.delete()
        new_entry.save()
        entry = new_entry
        # TODO get this logger working.
        logger.info(f'Pulled modified entry ({entry.title}) from disk into database.')
        print(f'INFO: Pulled modified entry ({entry.title}) from disk into database.')
    # Generate the HTML for this entry from the markdown (body).
    # TODO Consider caching. Probably misallocated effort.
    p = subprocess.Popen(
        'python prefilter.py --stdin | python filter.py | python -m markdown \
        -x markdown.extensions.nl2br -x markdown.extensions.fenced_code',
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    # TODO There is some odd newline thing happening here.
    out, _ = p.communicate(entry.body.encode('utf-8'))
    context = {'body': out.decode('utf-8')}  # This includes the header.
    return render(request, 'diary/entry.html', context)
