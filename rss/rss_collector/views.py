import email
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView
import pytz
from rss_collector.models import Sources, SourcesForm, Feeds, FeedsForm
from rss_collector.myparser import MyParser
from datetime import datetime, timedelta
from pytz import timezone
from rss import settings
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
        # form = SourcesForm(request.POST)
        # print(form_class)
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
    sources = Sources
    paginate_by = 20

    def get_context_data(self, **kwargs):
        all_sources = Sources.objects.get_queryset().all()
        feeds = {}
        posts = []
        for source in all_sources:
            myparser = MyParser(source.url)
            myparser.parse()
            feeds[source.url] = myparser.get_posts()
        for key in feeds:
            print(key)
            for value in feeds[key]:
                print(value['title'])
                print(value['link'])
                print(value['author'])
                print(value['published'])
                print(value['img'])
                posts.append(value)
        posts.sort(key=lambda r: r['published'], reverse=True)
        paginator = Paginator(posts, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        # feed_items = feedparser.parse(source.url)
        # print(feed_items)
        # for entry in feed_items['entries']:
        #     print("-------------------------")
        #     print(entry)
        #     print(entry.title)
        #     print(entry.link)
        #     try:
        #         entry.author
        #         print(entry['author'])
        #     except:
        #         pass
        #     # print(entry.author_detail.name)
        #     print(entry.published)
        #     try:
        #         entry['summary_detail']['value']
        #         print(entry['summary_detail']['value'])
        #         pattern = re.compile('http(.+?)"')
        #         img_src = pattern.search(entry['summary_detail']['value'])
        #         try:
        #             print("found")
        #             print(img_src.group()[:-1])
        #             print(img_src.group(0)[:-1])
        #         except:
        #             pass
        #     except:
        #         pass
        #     print("+++++++++++++++++++++++++++++++++")

        zagreb = timezone(settings.TIME_ZONE)
        f = Sources.objects.filter(id=1)
        print(f)
        k = Sources.objects.get(pk=1)
        print(k)
        print(datetime.now(zagreb))
        # print(timezone.now())
        print(k.feeds_set.all())

        dt = datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz("Thu, 24 Mar 2016 16:32:01 +0100")), zagreb)
        print(dt)
        print((datetime.now(zagreb) - dt) > timedelta(seconds=0))

        context = super(FeedsView, self).get_context_data(**kwargs)

        p = Feeds(sources="Sport24h", title="Nesreća: Kamion je istovarivao zemlju i pregazio vlasnika kuće", publish_time=dt, link="http://www.24sata.hr/news/nesreca-kamion-je-istovarivao-zemlju-i-pregazio-vlasnika-kuce-466767", author="Željko Rukavina", img_url="http://www.24sata.hr/media/img/e8/cb/42bf6010749bc9cac464.jpeg")
        p.save()
        # context["sources"] = self.model.objects.get_queryset().all()
        context["posts"] = posts
        return context
