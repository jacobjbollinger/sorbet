from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now as tz_utcnow
from django.utils.timezone import utc 

from celery.task import task
from feedparser import parse
from datetime import datetime

from .models import Feed
from .models import Item


@task
def fetch_all_feeds():
    feeds = Feed.objects.all()
    for feed in feeds:
        fetch_feed_items(feed)

@task
def fetch_feed_items(feed):
    parsed_feed = parse(feed.url)
    for item in parsed_feed.entries:
        try:
            Item.objects.get(feed=feed, guid=item.guid)
        except ObjectDoesNotExist:
            new_item = Item(
                feed = feed,
                pubdate = datetime(*(item.published_parsed[0:6]), tzinfo=utc),
                title = item.title,
                link = item.link,
                description = item.summary,
                guid = item.id,
            )
            #new_item.save()
            # TODO: Run task to send item to everyone subscribing to feed.

    feed.last_updated = datetime(*(parsed_feed.updated_parsed[0:6]), tzinfo=utc)
    feed.last_checked = tz_utcnow()
    feed.save()
