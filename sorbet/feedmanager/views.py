from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import md5

from bs4 import BeautifulSoup
from re import search
from urllib2 import urlopen
from urlparse import urlparse

from .models import Feed
from .forms import FeedForm
from .tasks import fetch_feed_items


@login_required
def featured(request):
    nofeed = True if request.GET.get("nofeed", None) else False

    template = u'feedmanager/featured.html'
    context = {
        'nofeed': nofeed
    }
    return TemplateResponse(request, template, context)


@login_required
def feeds(request):
    try:
        referer = request.META['HTTP_REFERER']
    except KeyError:
        pass
    else:
        if search('/accounts/register/$', request.META['HTTP_REFERER']):
            return HttpResponseRedirect(
                ''.join([reverse('feedmanager:featured'), '?nofeed=true']))

    feeds = Feed.objects.filter(users=request.user)
    form = FeedForm()

    template = u'feedmanager/feeds.html'
    context = {
        'feeds': feeds,
        'form': form,
    }
    return TemplateResponse(request, template, context)


@login_required
def add_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            # it's a very naive approach. we hash feeds' location with the username (if it's set)
            # and then store the hash in database. this hash should be unique for each tuple
            # (username, host, port). We then check feed's title to differentiate between feeds
            # on the same page. XXX: this will probably break at some point so think of a better
            # way to do that.
            url = urlparse(form.clean_url())
            feed_hash = md5.new(url.netloc)
            if url.username:
                feed_hash.update(url.username)
            feed_hash = feed_hash.hexdigest()
            try:
                feed = Feed.objects.get(hash=feed_hash)
            except Feed.DoesNotExist:
                feed = form.save(commit=False)
                feed.hash = feed_hash
                feed.save()
            else:
                soup = BeautifulSoup(urlopen(form.clean_url()).read())
                if soup.title.string != feed.title:
                    feed.save()
                else:
                    messages.warning(request, 'Feed already on the list!')

            feed.users.add(request.user)

            # Make sure the feed is up to date and send the user a preview...
            # To prevent new feeds from sending a blank preview.
            fetch_feed_items(feed, request.user)


            messages.success(request, 'New feed added successfully! Check your inbox for a preview of this feed.')
            return HttpResponseRedirect(reverse('feedmanager:feeds'))
        else:
            messages.error(request, 'Feed could not be added. We currently only support RSS feeds, make sure it is not an ATOM feed.')
            return HttpResponseRedirect(reverse('feedmanager:feeds'))


@login_required
def remove_feed(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    feed.users.remove(request.user)
    if len(feed.users.all()) == 0:
        feed.delete()
    messages.success(request, 'Feed successfully removed from your list!')
    return HttpResponseRedirect(reverse('feedmanager:feeds'))
