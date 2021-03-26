from django.urls import path

from shortlinksapp.views import main_page, links_history, short_links_redirect

urlpatterns = [
    path('', main_page, name='main-page'),
    path('history/', links_history, name='links-history'),
    path('u/<str:code>', short_links_redirect, name='short-links-redirect')
]
