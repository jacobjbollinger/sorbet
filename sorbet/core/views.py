from django.template.response import TemplateResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout

from .models import Feed


def home(request):
    template = u'core/home.html'
    context = None
    return TemplateResponse(request, template, context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New user created! Thank you for trying out Sorbet.')
            return HttpResponseRedirect(reverse('core:profile'))
        else:
            messages.error(request, 'There was a problem creating your user, please fix the items marked below.')
    else:
        form = UserCreationForm()

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
    feeds = Feed.objects.filter(users=request.user)

    template = u'core/feeds.html'
    context = {
        'feeds': feeds,
    }
    return TemplateResponse(request, template, context)


@login_required
def featured(request):
    template = u'core/featured.html'
    context = None
    return TemplateResponse(request, template, context)
