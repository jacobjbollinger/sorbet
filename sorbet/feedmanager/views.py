from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from re import search

from .models import Feed
from .forms import FeedForm


@login_required
def featured(request):
    try:
        if request.GET['nofeed'] == 'true': nofeed = True
    except:
        nofeed = False


    template = u'feedmanager/featured.html'
    context = {
        'nofeed': nofeed
    }
    return TemplateResponse(request, template, context)


@login_required
def feeds(request):
    feeds = Feed.objects.filter(users=request.user)
    form = FeedForm()

    if search('/accounts/login/$', request.META['HTTP_REFERER']) and not feeds:
        return HttpResponseRedirect(
            ''.join([reverse('feedmanager:featured'), '?nofeed=true']))

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
            try:
                feed = Feed.objects.get(url=form.clean_url())
            except Feed.DoesNotExist:
                feed = form.save(request.user)
            feed.users.add(request.user)
            messages.success(request, 'New feed added successfully!')
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
