# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Invitation.invited_at'
        db.add_column('core_invitation', 'invited_at',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Invitation.invited_at'
        db.delete_column('core_invitation', 'invited_at')

    models = {
        'core.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'invited_at': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'7666174c-a3b2-4d1b-b94b-81f8b5b1274f'", 'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']