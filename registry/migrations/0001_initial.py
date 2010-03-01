
from south.db import db
from django.db import models
from registry.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('registry_entry', (
            ('value_text', models.CharField(max_length=255, null=True, blank=True)),
            ('value_bool', models.BooleanField(null=True, blank=True)),
            ('key', models.CharField(unique=True, max_length=255)),
            ('value_numeric', models.IntegerField(null=True, blank=True)),
            ('type', models.CharField(default='T', max_length=1)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('registry', ['Entry'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('registry_entry')
        
    
    
    models = {
        'registry.entry': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'key': ('models.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'type': ('models.CharField', [], {'default': "'T'", 'max_length': '1'}),
            'value_bool': ('models.BooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_numeric': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['registry']
