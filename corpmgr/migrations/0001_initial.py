# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CorporationProfile'
        db.create_table('corpmgr_corporationprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('corporation', self.gf('django.db.models.fields.related.OneToOneField')(related_name='mgmt_profile', unique=True, to=orm['eveauth.Corporation'])),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(related_name='corps_managed', unique=True, to=orm['auth.User'])),
            ('director_group', self.gf('django.db.models.fields.related.OneToOneField')(related_name='directors_of', unique=True, to=orm['auth.Group'])),
            ('api_mask', self.gf('django.db.models.fields.IntegerField')()),
            ('reddit_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('corpmgr', ['CorporationProfile'])

        # Adding model 'Recommendation'
        db.create_table('corpmgr_recommendation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='app_recommendations', to=orm['account.Account'])),
            ('application_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('application_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('corpmgr', ['Recommendation'])

        # Adding model 'CorporationApplication'
        db.create_table('corpmgr_corporationapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('character', self.gf('django.db.models.fields.related.OneToOneField')(related_name='corp_app', unique=True, to=orm['eveauth.Character'])),
            ('corporation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_applications', to=orm['eveauth.Corporation'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='corporation_applications', to=orm['account.Account'])),
            ('reviewed_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='mbr_applications_reviewed', null=True, to=orm['account.Account'])),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='mbr_applications_approved', null=True, to=orm['account.Account'])),
            ('rejected_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='mbr_applications_rejected', null=True, to=orm['account.Account'])),
        ))
        db.send_create_signal('corpmgr', ['CorporationApplication'])

        # Adding unique constraint on 'CorporationApplication', fields ['character', 'corporation']
        db.create_unique('corpmgr_corporationapplication', ['character_id', 'corporation_id'])

        # Adding model 'AllianceApplication'
        db.create_table('corpmgr_allianceapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('corporation', self.gf('django.db.models.fields.related.OneToOneField')(related_name='alliance_application', unique=True, to=orm['eveauth.Corporation'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alliance_applications', to=orm['account.Account'])),
            ('reviewed_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='crp_applications_reviewed', null=True, to=orm['account.Account'])),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='crp_applications_approved', null=True, to=orm['account.Account'])),
            ('rejected_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='crp_applications_rejected', null=True, to=orm['account.Account'])),
        ))
        db.send_create_signal('corpmgr', ['AllianceApplication'])


    def backwards(self, orm):
        # Removing unique constraint on 'CorporationApplication', fields ['character', 'corporation']
        db.delete_unique('corpmgr_corporationapplication', ['character_id', 'corporation_id'])

        # Deleting model 'CorporationProfile'
        db.delete_table('corpmgr_corporationprofile')

        # Deleting model 'Recommendation'
        db.delete_table('corpmgr_recommendation')

        # Deleting model 'CorporationApplication'
        db.delete_table('corpmgr_corporationapplication')

        # Deleting model 'AllianceApplication'
        db.delete_table('corpmgr_allianceapplication')


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
        'corpmgr.allianceapplication': {
            'Meta': {'object_name': 'AllianceApplication'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'crp_applications_approved'", 'null': 'True', 'to': "orm['account.Account']"}),
            'corporation': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'alliance_application'", 'unique': 'True', 'to': "orm['eveauth.Corporation']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alliance_applications'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rejected_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'crp_applications_rejected'", 'null': 'True', 'to': "orm['account.Account']"}),
            'reviewed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'crp_applications_reviewed'", 'null': 'True', 'to': "orm['account.Account']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'corpmgr.corporationapplication': {
            'Meta': {'unique_together': "(('character', 'corporation'),)", 'object_name': 'CorporationApplication'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'mbr_applications_approved'", 'null': 'True', 'to': "orm['account.Account']"}),
            'character': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'corp_app'", 'unique': 'True', 'to': "orm['eveauth.Character']"}),
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_applications'", 'to': "orm['eveauth.Corporation']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'corporation_applications'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rejected_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'mbr_applications_rejected'", 'null': 'True', 'to': "orm['account.Account']"}),
            'reviewed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'mbr_applications_reviewed'", 'null': 'True', 'to': "orm['account.Account']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'corpmgr.corporationprofile': {
            'Meta': {'object_name': 'CorporationProfile'},
            'api_mask': ('django.db.models.fields.IntegerField', [], {}),
            'corporation': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mgmt_profile'", 'unique': 'True', 'to': "orm['eveauth.Corporation']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'director_group': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'directors_of'", 'unique': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'corps_managed'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'reddit_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'corpmgr.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'app_recommendations'", 'to': "orm['account.Account']"}),
            'application_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'application_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'eveauth.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'corp_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['corpmgr']