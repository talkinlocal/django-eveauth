# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field groups on 'AllianceProfile'
        db.delete_table('corpmgr_allianceprofile_groups')

        # Removing M2M table for field groups on 'CorporationProfile'
        db.delete_table('corpmgr_corporationprofile_groups')


    def backwards(self, orm):
        # Adding M2M table for field groups on 'AllianceProfile'
        db.create_table('corpmgr_allianceprofile_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('allianceprofile', models.ForeignKey(orm['corpmgr.allianceprofile'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('corpmgr_allianceprofile_groups', ['allianceprofile_id', 'group_id'])

        # Adding M2M table for field groups on 'CorporationProfile'
        db.create_table('corpmgr_corporationprofile_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('corporationprofile', models.ForeignKey(orm['corpmgr.corporationprofile'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('corpmgr_corporationprofile_groups', ['corporationprofile_id', 'group_id'])


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
            'corporation': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'alliance_application'", 'unique': 'True', 'to': "orm['eve_auth.Corporation']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alliance_applications'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rejected_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'crp_applications_rejected'", 'null': 'True', 'to': "orm['account.Account']"}),
            'reviewed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'crp_applications_reviewed'", 'null': 'True', 'to': "orm['account.Account']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'corpmgr.allianceprofile': {
            'Meta': {'object_name': 'AllianceProfile'},
            'alliance': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mgmt_profile'", 'unique': 'True', 'to': "orm['eve_auth.Alliance']"}),
            'api_mask': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'director_group': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'executive_directors_of'", 'unique': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alliances_managed'", 'to': "orm['auth.User']"})
        },
        'corpmgr.corporationapplication': {
            'Meta': {'unique_together': "(('character', 'corporation_profile'),)", 'object_name': 'CorporationApplication'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'mbr_applications_approved'", 'null': 'True', 'to': "orm['account.Account']"}),
            'character': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'corp_app'", 'unique': 'True', 'to': "orm['eve_auth.Character']"}),
            'corporation_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_applications'", 'to': "orm['corpmgr.CorporationProfile']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'corporation_applications'", 'to': "orm['account.Account']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rejected_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'mbr_applications_rejected'", 'null': 'True', 'to': "orm['account.Account']"}),
            'reviewed_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'mbr_applications_reviewed'", 'null': 'True', 'to': "orm['account.Account']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'corpmgr.corporationprofile': {
            'Meta': {'unique_together': "(('corporation', 'alliance_profile'),)", 'object_name': 'CorporationProfile'},
            'alliance_profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corp_profiles'", 'null': 'True', 'to': "orm['corpmgr.AllianceProfile']"}),
            'api_mask': ('django.db.models.fields.IntegerField', [], {}),
            'corporation': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mgmt_profile'", 'unique': 'True', 'to': "orm['eve_auth.Corporation']"}),
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
        'eve_auth.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'alliance_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'alliance_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'executor_of'", 'to': "orm['eve_auth.Corporation']"})
        },
        'eve_auth.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'apikeys'", 'to': "orm['account.Account']"}),
            'api_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eve_auth.character': {
            'Meta': {'object_name': 'Character'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_characters'", 'to': "orm['account.Account']"}),
            'api_key': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characters'", 'to': "orm['eve_auth.APIKey']"}),
            'character_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'character_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'corp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eve_auth.Corporation']"})
        },
        'eve_auth.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'corp_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['corpmgr']