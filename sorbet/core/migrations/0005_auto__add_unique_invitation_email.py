# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Invitation', fields ['email']
        db.create_unique('core_invitation', ['email'])

    def backwards(self, orm):
        # Removing unique constraint on 'Invitation', fields ['email']
        db.delete_unique('core_invitation', ['email'])

    models = {
        'core.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True'}),
            'invited_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'60cac10b-f285-4633-92f3-3d27ecc55a1e'", 'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']