from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import EmailUserCreationForm


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('feedmanager:feeds'))

    template = u'core/home.html'
    context = None
    return TemplateResponse(request, template, context)


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            user = form.save()
            user.is_active = True
            user.backend = "sorbet.core.backends.EmailAuthBackend"
            login(request, user)
            messages.success(request, 'New user created! Thank you for trying out Sorbet.')
            return HttpResponseRedirect(reverse('feedmanager:feeds'))
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
