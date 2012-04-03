# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invitation'
        db.create_table('core_invitation', (
            ('key', self.gf('django.db.models.fields.CharField')(default='0', max_length=32, primary_key=True)),
        ))
        db.send_create_signal('core', ['Invitation'])

    def backwards(self, orm):
        # Deleting model 'Invitation'
        db.delete_table('core_invitation')

    models = {
        'core.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'key': ('django.db.models.fields.CharField', [], {'default': "0", 'max_length': '32', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']
