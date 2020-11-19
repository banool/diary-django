from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect

from .models import (
    Entry,
    START,
)
from .util import (
    get_entry_from_file, 
    render_markdown,
    DATE_RE,
)

import logging
import os
import re
import time

logger = logging.getLogger(__name__)


def index(request):
    entries = Entry.objects.order_by('date')
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


def entry(request, title):
    entry = Entry.objects.get(title=title)
    if "no_auth_required" in entry.tags:
        pass
    elif not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # Get the entry. `title` is unique so this is works.
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
        logger.info(f'Pulled modified entry ({entry.title}) from disk into db.')
        print(f'INFO: Pulled modified entry ({entry.title}) from disk into db.')
    # Generate the HTML for this entry from the markdown (body).
    # TODO Consider caching. Probably misallocated effort.
    out = render_markdown(entry.body, username=request.user.username)
    # This includes the h1 header.
    context = {'body': out, 'title': title}
    return render(request, 'diary/entry.html', context)
