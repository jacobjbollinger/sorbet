from celery.task import task
from urlib2 import urlopen
from bs4 import BeautifulSoup

from .models import Item


@task
def fetch_feed_posts(feed):
    soup = BeautifulSoup(urlopen(feed).read())

    # TODO: The rest of this task.
