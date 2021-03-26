import datetime
import string
from django.shortcuts import render, redirect
from shortlinksapp.models import Links
from random import shuffle

SYMBOLS = list(string.ascii_lowercase)


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.html', {})
    else:
        [SYMBOLS.append(str(i)) for i in range(10)]
        while True:
            shuffle(SYMBOLS)
            short_link = str(request.build_absolute_uri()) + 'u/'
            for i in range(5):
                short_link += SYMBOLS[i]
            if not Links.objects.filter(short_link=short_link):
                Links.objects.create(
                    orig_link=request.POST.get('link'),
                    short_link=short_link,
                    datetime=str(datetime.datetime.now()),
                    clicks=0,
                )
                break
        return render(request, 'generated_link.html', {'link': short_link})


def links_history(request):
    links = Links.objects.all()
    return render(request, 'all_links.html', {'links': links})


def short_links_redirect(request, code):
    if Links.objects.filter(short_link=f'{str(request.build_absolute_uri())}'):
        orig_link = Links.objects.get(short_link=f'{str(request.build_absolute_uri())}')
        orig_link.clicks += 1
        orig_link.save()
        return redirect(f'{orig_link.orig_link}')
    else:
        return render(request, 'error.html', {'link': str(request.build_absolute_uri())})
