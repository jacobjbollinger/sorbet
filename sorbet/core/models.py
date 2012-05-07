import datetime

from uuid import uuid4

from django.conf import settings
from django.db import models

class InvitationManager(models.Manager):
    def limit_reached(self):
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        qs = super(InvitationManager, self).get_query_set()
        return qs.filter(invited_at__gte=last_monday).count() > settings.INVITES_PER_WEEK

class Invitation(models.Model):
    def _create_uuid():
        return str(uuid4())

    objects = InvitationManager()

    key = models.CharField(max_length=36, default=_create_uuid, primary_key=True)
    invited_at = models.DateField(auto_now_add=True, null=True)
    email = models.EmailField(null=True)