from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.core.exceptions import ObjectDoesNotExist

from .models import Feed
from .forms import FeedForm
from .forms import EmailUserCreationForm


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('core:feeds'))

    template = u'core/home.html'
    context = None
    return TemplateResponse(request, template, context)


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New user created! Thank you for trying out Sorbet.')
            return HttpResponseRedirect(reverse('core:feeds'))
    else:
        form = EmailUserCreationForm()

    template = u'core/register.html'
    context = {
        'form': form,
    }
    return TemplateResponse(request, template, context)


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'We hope to see you again soon! Enjoy the feeds.')
    return HttpResponseRedirect(reverse('core:home'))


@login_required
def featured(request):
    template = u'core/featured.html'
    context = None
    return TemplateResponse(request, template, context)


@login_required
def feeds(request):
    feeds = Feed.objects.filter(users=request.user)
    form = FeedForm()

    template = u'core/feeds.html'
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
            except ObjectDoesNotExist:
                feed = form.save(request.user)
            feed.users.add(request.user)
            messages.success(request, 'New feed added successfully!')
            return HttpResponseRedirect(reverse('core:feeds'))
        else:
            messages.error(request, 'Feed could not be added. We currently only support RSS feeds, make sure it is not an ATOM feed.')
            return HttpResponseRedirect(reverse('core:feeds'))


@login_required
def remove_feed(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    feed.users.remove(request.user)
    if len(feed.users.all()) == 0:
        feed.delete()
    messages.success(request, 'Feed successfully removed from your list!')
    return HttpResponseRedirect(reverse('core:feeds'))
