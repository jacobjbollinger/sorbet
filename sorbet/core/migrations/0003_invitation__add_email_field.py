# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Invitation.email'
        db.add_column('core_invitation', 'email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Invitation.email'
        db.delete_column('core_invitation', 'email')

    models = {
        'core.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'1a9f6150-2768-472b-ad21-f3b171931cc8'", 'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']