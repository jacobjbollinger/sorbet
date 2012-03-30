from django.utils.timezone import now as tz_utcnow
from django.utils.timezone import utc
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery.task import task
from feedparser import parse
from datetime import datetime

from .models import Item


@task
def fetch_feed_items(feed, user=None):
    parsed_feed = parse(feed.url)
    for item in parsed_feed.entries:
        try:
            Item.objects.get(feed=feed, guid=item.guid)
        except Item.DoesNotExist:
            new_item = Item(
                feed = feed,
                pubdate = datetime(*(item.published_parsed[0:6]), tzinfo=utc),
                title = item.title,
                link = item.link,
                description = item.summary,
                guid = item.id,
            )
            new_item.save()

            if feed.last_checked != None:
                send_new_item(feed.users.all(), new_item, feed.title)

    if user: send_preview(user, feed)

    feed.last_updated = datetime(*(parsed_feed.updated_parsed[0:6]), tzinfo=utc)
    feed.last_checked = tz_utcnow()
    feed.save()


@task
def send_new_item(users, item, feed_title):
    for user in users:
        subject = ''.join(['[', feed_title, '] ', item.title])
        from_email = 'Sorbet <noreply@sorbetapp.com>'
        to = user.email

        html_content = render_to_string('feedmanager/email/new_item.html',
            { 'item': item })
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@task
def send_preview(user, feed):
    subject = ''.join(['Subscribed to ', feed.title])
    from_email = 'Sorbet <noreply@sorbetapp.com>'
    to = user.email

    html_content = render_to_string('feedmanager/email/feed_preview.html',
        { 'item_list': feed.item_set.all()[:3] })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
