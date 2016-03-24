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

    # def add_arguments(self, parser):
    #     parser.add_argument('feeds_id', nargs='+', type=int)

    def handle(self, *args, **options):
        feeds = {}
        posts = []
        zagreb = timezone(settings.TIME_ZONE)
        all_sources = Sources.objects.get_queryset().all()
        for source in all_sources:
            myparser = MyParser(source.url)
            myparser.parse()
            feeds[source.url] = myparser.get_posts()
            for key in feeds:
                for value in feeds[key]:
                    # print(value['title'])
                    # print(value['link'])
                    # print(value['author'])
                    print(datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(value['published'])), zagreb))
                    # dd = datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(value['published'])), zagreb)
                    # print(value['img'])
                    posts.append(value)
            dt = datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz("Thu, 24 Mar 2016 16:32:01 +0100")), zagreb)
            p = Feeds(sources=Sources.objects.get(pk=1), title="Nesreća: Kamion je istovarivao zemlju i pregazio vlasnika kuće", publish_time=dt, link="http://www.24sata.hr/news/nesreca-kamion-je-istovarivao-zemlju-i-pregazio-vlasnika-kuce-466767", author="Željko Rukavina", img_url="http://www.24sata.hr/media/img/e8/cb/42bf6010749bc9cac464.jpeg")
            p.save()




        # for feeds_id in options['feeds_id']:

            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)

            # poll.opened = False
            # poll.save()

            # self.stdout.write(self.style.SUCCESS('Feeds successfully updated "%s"' % feed_id))
