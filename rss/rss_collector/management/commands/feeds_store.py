from django.core.management.base import BaseCommand, CommandError

from rss_collector.models import Feeds

class Command(BaseCommand):
    help = 'Stores active posts to db'
    args = 'Arguments are not needed'

    # def add_arguments(self, parser):
    #     parser.add_argument('feeds_id', nargs='+', type=int)

    def handle(self, *args, **options):
        
        # for feeds_id in options['feeds_id']:

            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)

            # poll.opened = False
            # poll.save()

            # self.stdout.write(self.style.SUCCESS('Feeds successfully updated "%s"' % feed_id))
