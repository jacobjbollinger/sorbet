# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Invitation.key'
        db.alter_column('core_invitation', 'key', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True))
    def backwards(self, orm):

        # Changing field 'Invitation.key'
        db.alter_column('core_invitation', 'key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True))
    models = {
        'core.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'key': ('django.db.models.fields.CharField', [], {'default': "'5277865e-a98b-4448-9338-0795cad16b46'", 'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']