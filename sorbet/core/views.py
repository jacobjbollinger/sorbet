from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

from .forms import EmailUserCreationForm
from .models import Invitation


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('feedmanager:feeds'))

    template = u'core/home.html'
    context = None
    return TemplateResponse(request, template, context)


def register(request):
    if request.method == 'POST':
        key = request.session.get("invitation_key", None)
        if settings.INVITE_ONLY and not Invitation.objects.filter(key=key).exists():
            return HttpResponse403
        post_data = request.POST.copy()
        if request.session["invitation_email"]:
            post_data['email'] = request.session["invitation_email"]
        form = EmailUserCreationForm(post_data)
        if form.is_valid():
            from django.contrib.auth import login
            user = form.save()
            user.is_active = True
            user.backend = "sorbet.core.backends.EmailAuthBackend"
            login(request, user)
            messages.success(request, 'New user created! Thank you for trying out Sorbet.')
            if key:
                Invitation.objects.filter(key=key).delete()
            return HttpResponseRedirect(reverse('feedmanager:feeds'))
    else:
        key = request.GET.get('key', None)
        if settings.INVITE_ONLY:
            try:
                invitation = Invitation.objects.filter(key=key).get()
            except Invitation.DoesNotExist:
                messages.error(request, "Sorry, invitation is required at this time for our hosted version. <a href=\"https://github.com/overshard/sorbet/\">Clone us on GitHub</a> instead and host Sorbet yourself!")
                return HttpResponseRedirect(reverse('core:home'))
            else:
                request.session["invitation_key"] = invitation.key
                request.session["invitation_email"] = invitation.email
        else:
            request.session["invitation_email"] = None
        form = EmailUserCreationForm(initial={'email': request.session["invitation_email"]})
        if request.session["invitation_email"]:
            # disable email field when email was set from the invitation
            form.fields['email'].widget.attrs['readonly'] = True
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
