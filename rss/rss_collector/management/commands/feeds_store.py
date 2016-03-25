from django.core.management.base import BaseCommand, CommandError
import email
from rss_collector.models import Feeds, Sources
from rss_collector.myparser import MyParser
from pytz import timezone
from rss import settings
from datetime import datetime


class Command(BaseCommand):
    help = 'Stores active posts to db'
    args = 'Arguments are not needed'

    def handle(self, *args, **options):
        feeds = {}
        zagreb = timezone(settings.TIME_ZONE)
        all_sources = Sources.objects.get_queryset().all()

        #hardcode some sources if source table is empty, easier to use while controlling task
        if not all_sources:
            all_sources = [
                Sources(name="Sport24h", url="http://www.24sata.hr/feeds/sport.xml"),
                Sources(name="NajnovijePoslovni", url="http://www.poslovni.hr/feeds/najnovije.xml"),
                Sources(name="Najnovije24h", url="http://www.24sata.hr/feeds/najnovije.xml")
            ]
            for source in all_sources:
                source.save()

        for source in all_sources:
            myparser = MyParser(source.url)
            myparser.parse()
            feeds[source.url] = myparser.get_posts()
            for key in feeds:
                for value in feeds[key]:
                    if not Feeds.objects.filter(link=value['link']).filter(title=value['title']).exists():
                        s = source
                        t = value['title']
                        pd = datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(value['published'])), zagreb)
                        l = value['link']
                        a = value['author']
                        i = value['img']
                        p = Feeds(sources=s, title=t, publish_time=pd, link=l, author=a, img_url=i)
                        p.save()
        self.stdout.write("Feeds table updated")
