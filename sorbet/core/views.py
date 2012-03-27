from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout

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
            messages.error(request, 'There was a problem creating your user, please fix the items marked below.')
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
def feeds(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
    else:
        form = FeedForm()

    feeds = Feed.objects.filter(users=request.user)

    template = u'core/feeds.html'
    context = {
        'form': form,
        'feeds': feeds,
    }
    return TemplateResponse(request, template, context)


@login_required
def featured(request):
    template = u'core/featured.html'
    context = None
    return TemplateResponse(request, template, context)
