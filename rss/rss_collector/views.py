from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import FormView, TemplateView, ListView
from rss_collector.models import Sources, SourcesForm, Feeds

import simplejson

# Create your views here.


class IndexView(FormView):
    model = Sources
    template_name = "index.html"
    form_class = SourcesForm

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
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
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
        # sort array
        # posts.sort(key=lambda r: r['published'], reverse=True)

        # hardcoded
        if self.sources.all():
            allowed_source = self.sources.order_by('?').first()
        else:
            allowed_source = Sources(name="Sport24h", url="http://www.24sata.hr/feeds/sport.xml")

        posts = self.feeds.all().order_by('-publish_time')
        linked_posts = self.feeds.filter(sources=allowed_source).order_by('-publish_time')

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

        context = super(FeedsView, self).get_context_data(**kwargs)
        context["posts"] = posts
        context["linked_posts"] = linked_posts
        return context


class SearchView(ListView):
    feeds = Feeds.objects
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        authors_model = []
        authors_value ={}
        context = super(SearchView, self).get_context_data(**kwargs)

        all_authors = self.feeds.all().values('author').distinct()

        for author in all_authors:
            authors_value['value'] = author['author']
            authors_model.append(authors_value)
            authors_value = {}

        context['authors'] = simplejson.dumps(authors_model)
        context['authors'] = authors_model
        context["object_list"] = self.get_queryset()
        return context

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
