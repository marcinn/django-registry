# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ModelEntry'
        db.create_table('registry_modelentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='T', max_length=1)),
            ('value_bool', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('value_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('value_numeric', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('registry', ['ModelEntry'])

        # Changing field 'Entry.value_bool'
        db.alter_column('registry_entry', 'value_bool', self.gf('django.db.models.fields.NullBooleanField')(null=True))


    def backwards(self, orm):
        
        # Deleting model 'ModelEntry'
        db.delete_table('registry_modelentry')

        # Changing field 'Entry.value_bool'
        db.alter_column('registry_entry', 'value_bool', self.gf('models.BooleanField')(null=True))


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'registry.entry': {
            'Meta': {'object_name': 'Entry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_numeric': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'registry.modelentry': {
            'Meta': {'object_name': 'ModelEntry'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_numeric': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['registry']
