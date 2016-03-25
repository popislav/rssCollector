from django.conf.urls import url
from django.views.generic import RedirectView
from rss_collector.views import IndexView, FeedsView, SearchView

from . import views

urlpatterns = [
    url(r'^sources$', IndexView.as_view(), name='sources'),
    url(r'^posts$', FeedsView.as_view(), name='posts'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^.*$', RedirectView.as_view(url='sources', permanent=False), name='index')

]
