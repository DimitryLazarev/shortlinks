import datetime
import string

from django.shortcuts import render, redirect
from django.urls import NoReverseMatch
from shortlinksapp.forms import PersonalLinkForm, LinkForm
from shortlinksapp.models import Links
from random import shuffle

SYMBOLS = list(string.ascii_lowercase + string.digits)


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.html', {'form': LinkForm()})
    else:
        form = LinkForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            while True:
                shuffle(SYMBOLS)
                short_link = str(request.build_absolute_uri()) + 'u/'
                for i in range(5):
                    short_link += SYMBOLS[i]
                if not Links.objects.filter(short_link=short_link):
                    Links.objects.create(
                        orig_link=cd.get('full_link'),
                        short_link=short_link,
                        datetime=str(datetime.datetime.now()),
                        clicks=0,
                    )
                    break
            return render(request, 'generated_link.html', {'link': short_link, 'form': form})
        else:
            return render(request, 'main.html', {'err': form})


def links_history(request):
    links = Links.objects.all()
    return render(request, 'all_links.html', {'links': links})


def short_links_redirect(request, code):
    if Links.objects.filter(short_link=f'{str(request.build_absolute_uri())}'):
        orig_link = Links.objects.get(short_link=f'{str(request.build_absolute_uri())}')
        orig_link.clicks += 1
        orig_link.save()
        try:
            return redirect(f'{orig_link.orig_link}')
        except NoReverseMatch as err:
            return render(request, 'NoReverseMatch.html', {'link': orig_link.orig_link})
    else:
        return render(request, 'error.html', {'link': str(request.build_absolute_uri())})


def personal_link(request):
    if request.method == 'GET':
        return render(
            request,
            'personal_link.html',
            {'form': PersonalLinkForm(initial={'short_link': '/'.join(request.build_absolute_uri().split('/')[:-2]) + '/u/'})}
        )
    else:
        form = PersonalLinkForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not Links.objects.filter(short_link=cd.get('short_link')):
                Links.objects.create(
                    orig_link=cd.get('full_link'),
                    short_link=cd.get('short_link'),
                    datetime=str(datetime.datetime.now()),
                    clicks=0,
                )
                return render(request,
                              'generated_personal_link.html', {
                                  'full_link': cd.get('full_link'),
                                  'personal_link': cd.get('short_link'),
                                  'form': PersonalLinkForm(initial={'short_link': '/'.join(request.build_absolute_uri().split('/')[:-2]) + '/u/'}),
                              }
                              )
            else:
                return render(
                    request,
                    'personal_link.html',
                    {'form': PersonalLinkForm(initial={'short_link': '/'.join(str(request.build_absolute_uri()).split('/')[:-2]) + '/u/'}),
                     'already_in_list_err': True
                     }
                              )
        else:
            return render(request, 'personal_link.html', {'form': form})
