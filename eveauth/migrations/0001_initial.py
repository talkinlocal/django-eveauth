# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'APIKey'
        db.create_table('eveauth_apikey', (
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='apikeys', to=orm['account.Account'])),
            ('api_id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('vcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('eveauth', ['APIKey'])

        # Adding model 'Corporation'
        db.create_table('eveauth_corporation', (
            ('corp_id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('eveauth', ['Corporation'])

        # Adding model 'Character'
        db.create_table('eveauth_character', (
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='all_characters', to=orm['account.Account'])),
            ('api_key', self.gf('django.db.models.fields.related.ForeignKey')(related_name='characters', to=orm['eveauth.APIKey'])),
            ('character_id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('corp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eveauth.Corporation'])),
            ('character_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('eveauth', ['Character'])

        # Adding model 'CharacterSheet'
        db.create_table('eveauth_charactersheet', (
            ('character', self.gf('django.db.models.fields.related.OneToOneField')(related_name='sheet', unique=True, primary_key=True, to=orm['eveauth.Character'])),
            ('corp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eveauth.Corporation'])),
            ('alliance_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sec_status', self.gf('django.db.models.fields.IntegerField')()),
            ('last_retrieved', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('eveauth', ['CharacterSheet'])

        # Adding model 'DefaultCharacter'
        db.create_table('eveauth_defaultcharacter', (
            ('account', self.gf('django.db.models.fields.related.OneToOneField')(related_name='default_character', unique=True, to=orm['account.Account'])),
            ('character', self.gf('django.db.models.fields.related.OneToOneField')(related_name='default_for', unique=True, primary_key=True, to=orm['eveauth.Character'])),
        ))
        db.send_create_signal('eveauth', ['DefaultCharacter'])

        # Adding unique constraint on 'DefaultCharacter', fields ['account', 'character']
        db.create_unique('eveauth_defaultcharacter', ['account_id', 'character_id'])

        # Adding model 'Alliance'
        db.create_table('eveauth_alliance', (
            ('alliance_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('executor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='executor_of', to=orm['eveauth.Corporation'])),
        ))
        db.send_create_signal('eveauth', ['Alliance'])


    def backwards(self, orm):
        # Removing unique constraint on 'DefaultCharacter', fields ['account', 'character']
        db.delete_unique('eveauth_defaultcharacter', ['account_id', 'character_id'])

        # Deleting model 'APIKey'
        db.delete_table('eveauth_apikey')

        # Deleting model 'Corporation'
        db.delete_table('eveauth_corporation')

        # Deleting model 'Character'
        db.delete_table('eveauth_character')

        # Deleting model 'CharacterSheet'
        db.delete_table('eveauth_charactersheet')

        # Deleting model 'DefaultCharacter'
        db.delete_table('eveauth_defaultcharacter')

        # Deleting model 'Alliance'
        db.delete_table('eveauth_alliance')


    models = {
        'account.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '10'}),
            'timezone': ('account.fields.TimeZoneField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'account'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eveauth.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'alliance_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'executor_of'", 'to': "orm['eveauth.Corporation']"})
        },
        'eveauth.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'apikeys'", 'to': "orm['account.Account']"}),
            'api_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eveauth.character': {
            'Meta': {'object_name': 'Character'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_characters'", 'to': "orm['account.Account']"}),
            'api_key': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characters'", 'to': "orm['eveauth.APIKey']"}),
            'character_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'character_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'corp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eveauth.Corporation']"})
        },
        'eveauth.charactersheet': {
            'Meta': {'object_name': 'CharacterSheet'},
            'alliance_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'character': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'sheet'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['eveauth.Character']"}),
            'corp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eveauth.Corporation']"}),
            'last_retrieved': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sec_status': ('django.db.models.fields.IntegerField', [], {})
        },
        'eveauth.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'corp_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'eveauth.defaultcharacter': {
            'Meta': {'unique_together': "(('account', 'character'),)", 'object_name': 'DefaultCharacter'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'default_character'", 'unique': 'True', 'to': "orm['account.Account']"}),
            'character': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'default_for'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['eveauth.Character']"})
        }
    }

    complete_apps = ['eveauth']