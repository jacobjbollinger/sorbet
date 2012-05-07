import feedparser

from django.utils.timezone import now as tz_utcnow
from django.utils.timezone import utc
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery.task import task
from celery.task.sets import subtask

from datetime import (datetime,
                      timedelta)

from .models import Item

@task
def update_feeds(feed, user=None, callback=None):
    new_items = False
    parsed_feed = feedparser.parse(feed.url)
    for item in parsed_feed.entries:
        try:
            Item.objects.get(feed=feed, guid=item.guid)
        except Item.DoesNotExist:
            new_items = True

            try:
                date = datetime(*(item.published_parsed[0:6]), tzinfo=utc)
            except AttributeError:
                date = datetime(*(item.updated_parsed[0:6]), tzinfo=utc)

            Item.objects.create(feed=feed, pubdate=date, title=item.title,
                                link=item.link, description=item.summary, guid=item.id)

    feed.last_checked = tz_utcnow()
    if new_items:
        feed.last_updated = tz_utcnow()

    feed.save()

    if callback:
        subtask(callback).delay()


@task
def send_email(user, content, preview=False, callback=None):
    subject = u'Updates from your Sorbet!'
    from_email = 'Sorbet <noreply@sorbetapp.com>'
    to = user.email

    if preview:
        template = 'feedmanager/email/feed_preview.html'
        context = {'feed': content}
    else:
        template = 'feedmanager/email/new_items.html'
        context = {'feeds': content}

    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    if callback:
        subtask(callback).delay()

@task
def prepare_preview_email(user, feed):
    update_feeds.delay(feed, user, callback=send_email.subtask((user, feed, True)))


def get_updates_for_user(user, now):
    return user.feed_set.filter(last_updated__lte=now).all()

@task
def reschedule_update(user, current_time):
    user.scheduled_update = current_time + timedelta(hours=user.get_profile().email_frequency)
    user.save()

@task
def send_updates():
    now = tz_utcnow()
    users = User.objects.filter(userprofile__scheduled_update__lte=now).all()
    for user in users:
        updated_feeds = get_updates_for_user(user, now)
        send_email.delay(user, updated_feeds, callback=reschedule_update.subtask((user, now)))
