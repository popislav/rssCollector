from django.conf.urls import url
from rss_collector.views import IndexView, FeedsView

from . import views

urlpatterns = [
    url(r'^sources$', IndexView.as_view()),
    url(r'^posts$', FeedsView.as_view())
]
