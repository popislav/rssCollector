from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView
from rss_collector.models import Sources, SourcesForm
from rss_collector.myparser import MyParser
import datetime
from django.utils import timezone
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
                print(value['published'])
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

        f = Sources.objects.filter(id=1)
        print(f)
        k = Sources.objects.filter(pk=1)
        print(k)
        print(datetime.datetime.now())
        print(timezone.now())
        # print(k.feeds_set.all())

        context = super(FeedsView, self).get_context_data(**kwargs)
        # context["sources"] = self.model.objects.get_queryset().all()
        context["posts"] = posts
        return context
