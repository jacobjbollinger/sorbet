from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import md5

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import urlparse

from .models import Feed
from .forms import FeedForm
import feedmanager.tasks as feed_tasks

def featured(request):
    template = u'feedmanager/featured.html'
    context = {
        'tutorial': True if request.GET.get('tutorial', None) else False
    }
    return TemplateResponse(request, template, context)


@login_required
def feeds(request):
    if urlparse(request.META.get('HTTP_REFERER') or '/').path == '/accounts/register/':
        return HttpResponseRedirect(''.join([reverse('feedmanager:featured'), '?tutorial=true']))


    template = u'feedmanager/feeds.html'
    context = {
        'feeds': Feed.objects.filter(users=request.user),
        'form': FeedForm(),
    }
    return TemplateResponse(request, template, context)


@login_required
def add_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            url = urlparse(form.clean_url())
            feed_hash = md5.new(url.netloc)
            feed_hash.update(url.path)
            if url.username: feed_hash.update(url.username)
            feed_hash = feed_hash.hexdigest()

            try:
                feed = Feed.objects.get(hash=feed_hash)
            except Feed.DoesNotExist:
                feed = form.save(commit=False)
                feed.hash = feed_hash
                feed.save()

            feed.users.add(request.user)

            # work around bs4.element.NavigableString not being serializable
            feed.title = unicode(feed.title)

            feed_tasks.prepare_preview_email(request.user, feed)

            messages.success(request, 'New feed added successfully. Check your inbox for a preview of this feed!')
        else:
            messages.error(request, 'Only RSS and ATOM URLs/feeds are currently supported.')

    return HttpResponseRedirect(reverse('feedmanager:feeds'))


@login_required
def remove_feed(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    feed.users.remove(request.user)
    if len(feed.users.all()) == 0: feed.delete()

    messages.success(request, 'Feed successfully removed from your list!')
    return HttpResponseRedirect(reverse('feedmanager:feeds'))
