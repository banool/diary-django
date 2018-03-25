from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Entry


def index(request):
    entries = Entry.objects.order_by('-date')
    context = {'entries': entries}
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
    context = {'title': entry.title, 'body': entry.body}
    return render(request, 'diary/entry.html', context)
