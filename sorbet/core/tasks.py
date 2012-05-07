from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery.task import task

from .models import Invitation

@task
def send_invitations(how_many):
    invites = Invitation.objects.filter(sent=False).order_by('invited_at')[:how_many].all()
    sent_ids = []
    for invite in invites:
        subject = u'Sorbet invitation!'
        from_email = 'Sorbet <noreply@sorbetapp.com>'
        to = invite.email

        template = 'core/email/invitation.html'
        context = {'key': invite.key}

        html_content = render_to_string(template, context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        sent_ids.append(invite.pk)
    Invitation.objects.filter(pk__in=sent_ids).update(sent=True)