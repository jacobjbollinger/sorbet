from uuid import uuid4

from django.db import models

class Invitation(models.Model):
    def _create_uuid():
        return str(uuid4())

    key = models.CharField(max_length=32, default=_create_uuid, primary_key=True)
