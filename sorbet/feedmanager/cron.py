from cronjobs import register

from .models import Feed
from .tasks import fetch_feed_items


@register
def fetch_all_feeds():
    feeds = Feed.objects.all()
    for feed in feeds:
        fetch_feed_items(feed)
