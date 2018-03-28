from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Entry, START

import re

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
    context = {'body': entry.body}  # This includes the header.
    return render(request, 'diary/entry.html', context)
