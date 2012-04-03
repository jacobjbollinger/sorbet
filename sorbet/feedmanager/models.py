from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from urllib2 import urlopen
from bs4 import BeautifulSoup


class Feed(models.Model):
    users = models.ManyToManyField(User)
    url = models.TextField(_('URL'))
    hash = models.CharField(max_length=32)
    title = models.CharField(_('title'), max_length=70)
    added = models.DateTimeField(_('added'), auto_now_add=True)
    last_checked = models.DateTimeField(_('last checked'), blank=True, null=True)
    last_updated = models.DateTimeField(_('last updated'), blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.title:
            soup = BeautifulSoup(urlopen(self.url).read())
            self.title = soup.title.string
        super(Feed, self).save()


class Item(models.Model):
    feed = models.ForeignKey(Feed)
    added = models.DateTimeField(_('added'), auto_now_add=True)
    pubdate = models.DateTimeField(_('published'))
    title = models.CharField(_('title'), max_length=70)
    link = models.TextField(_('link'))
    description = models.TextField(_('description'))
    guid = models.CharField(_('GUID'), max_length=128)

    def __unicode__(self):
        return self.title
