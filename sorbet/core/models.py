from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Feed(models.Model):
    users = models.ManyToManyField(User)
    url = models.CharField(_('url'), max_length=128)
    title = models.CharField(_('title'), max_length=70)
    added = models.DateTimeField(_('added'), auto_now_add=True)
    last_updated = models.DateTimeField(_('last updated'))

    def __unicode__(self):
        return self.title


class Item(models.Model):
    feed = models.ForeignKey(Feed)
    published = models.DateTimeField(_('published'))
    added = models.DateTimeField(_('added'), auto_now_add=True)

    def __unicode__(self):
        return self.feed
