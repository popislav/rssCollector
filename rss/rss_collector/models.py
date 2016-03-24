from django.db import models
from django.forms import ModelForm
from datetime import datetime


# Create your models here.


class Sources(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class SourcesForm(ModelForm):
    class Meta:
        model = Sources
        fields = ['name', 'url']


class Feeds(models.Model):
    sources = models.ForeignKey(Sources, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    publish_time = models.DateTimeField(blank=True, null=True, default=datetime.now)
    link = models.URLField(max_length=300)
    author = models.TextField(max_length=200)
    img_url = models.URLField(max_length=300)

    def __str__(self):
        return self.title


class FeedsForm(ModelForm):
    class Meta:
        model = Feeds
        fields = ['sources', 'title', 'publish_time', 'link', 'author', 'img_url']

