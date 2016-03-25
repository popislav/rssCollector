import email
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView, ListView
import pytz
from rss_collector.models import Sources, SourcesForm, Feeds, FeedsForm

from django.core import serializers

# from django.utils import simplejson

import simplejson

from rss_collector.myparser import MyParser
from datetime import datetime, timedelta
from pytz import timezone
from rss import settings
# from easy_thumbnails.files import get_thumbnailer
from django.shortcuts import render

# Create your views here.


class IndexView(FormView):
    model = Sources
    template_name = "index.html"
    form_class = SourcesForm

    # def get(self, request, *args, **kwargs):
    #     self.get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["sources"] = self.model.objects.get_queryset().all()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print(form)
        if form.is_valid(**kwargs):
            return self.form_valid(form, **kwargs)
        else:
            return  self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        # name = form.cleaned_data['name']
        # url = form.cleaned_data['url']
        context = self.get_context_data(**kwargs)
        form.save()
        return self.render_to_response(context)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context["invalid_form"] = "The form was invalid, please fill it again (aka. write the sources name and url)"
        return self.render_to_response(context)


class FeedsView(TemplateView):
    template_name = "news.html"
    sources = Sources.objects
    feeds = Feeds.objects
    paginate_by = 20

    def get_context_data(self, **kwargs):

        # value['img'] = get_thumbnailer(value['img'])['avatar'].url

        # sort array
        # posts.sort(key=lambda r: r['published'], reverse=True)

        # hardcoded
        if self.sources.filter(pk=1).exists():
            allowed_feed = self.sources.get(pk=1)
        else:
            allowed_feed = "http://www.24sata.hr/feeds/sport.xml"

        posts = self.feeds.all()
        linked_posts = self.feeds.filter(sources=allowed_feed)

        ###paginator part
        paginator = Paginator(posts, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        ###


        # f = Sources.objects.filter(id=1)
        # k = Sources.objects.get(pk=1)
        # print(k.feeds_set.all())
        # print((datetime.now(zagreb) - dt) > timedelta(seconds=0))

        context = super(FeedsView, self).get_context_data(**kwargs)

        # p = Feeds(sources=Sources.objects.get(pk=1), title="Nesreća: Kamion je istovarivao zemlju i pregazio vlasnika kuće", publish_time=dt, link="http://www.24sata.hr/news/nesreca-kamion-je-istovarivao-zemlju-i-pregazio-vlasnika-kuce-466767", author="Željko Rukavina", img_url="http://www.24sata.hr/media/img/e8/cb/42bf6010749bc9cac464.jpeg")
        # p.save()

        # context["sources"] = self.model.objects.get_queryset().all()
        context["posts"] = posts
        context["linked_posts"] = linked_posts
        return context


class SearchView(ListView):
    feeds = Feeds.objects
    template_name = "search.html"

    # def get(self, request, *args, **kwargs):
    #     self.get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        authors_model = []
        authors_value ={}
        context = super(SearchView, self).get_context_data(**kwargs)

        all_authors = self.feeds.all().values('author').distinct()
        for author in all_authors:
            authors_value['value'] = author['author']
            authors_model.append(authors_value)
            authors_value = {}
        print(authors_model)

        context['authors'] = simplejson.dumps(authors_model)
        context["object_list"] = self.get_queryset()
        return context
        # return HttpResponse(context, content_type='application/json')

    def get_queryset(self):
        try:
            name = self.request.GET.get('name')
        except:
            name = ''
        if name != '':
            object_list = self.feeds.filter(author=name)
        else:
            object_list = self.feeds.all()
        return object_list




    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     print(form)
    #     if form.is_valid(**kwargs):
    #         return self.form_valid(form, **kwargs)
    #     else:
    #         return  self.form_invalid(form, **kwargs)
