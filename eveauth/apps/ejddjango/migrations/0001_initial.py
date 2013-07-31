# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table('ejddjango_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ejddjango', ['Domain'])

        # Adding model 'UserJID'
        db.create_table('ejddjango_userjid', (
            ('site_user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='jid', unique=True, primary_key=True, to=orm['auth.User'])),
            ('node', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jids', to=orm['ejddjango.Domain'])),
        ))
        db.send_create_signal('ejddjango', ['UserJID'])

        # Adding unique constraint on 'UserJID', fields ['node', 'domain']
        db.create_unique('ejddjango_userjid', ['node', 'domain_id'])

        # Adding model 'SharedRosterGroup'
        db.create_table('ejddjango_sharedrostergroup', (
            ('site_group', self.gf('django.db.models.fields.related.OneToOneField')(related_name='srg', unique=True, primary_key=True, to=orm['auth.Group'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ejddjango.Domain'])),
        ))
        db.send_create_signal('ejddjango', ['SharedRosterGroup'])

        # Adding M2M table for field members on 'SharedRosterGroup'
        db.create_table('ejddjango_sharedrostergroup_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sharedrostergroup', models.ForeignKey(orm['ejddjango.sharedrostergroup'], null=False)),
            ('userjid', models.ForeignKey(orm['ejddjango.userjid'], null=False))
        ))
        db.create_unique('ejddjango_sharedrostergroup_members', ['sharedrostergroup_id', 'userjid_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserJID', fields ['node', 'domain']
        db.delete_unique('ejddjango_userjid', ['node', 'domain_id'])

        # Deleting model 'Domain'
        db.delete_table('ejddjango_domain')

        # Deleting model 'UserJID'
        db.delete_table('ejddjango_userjid')

        # Deleting model 'SharedRosterGroup'
        db.delete_table('ejddjango_sharedrostergroup')

        # Removing M2M table for field members on 'SharedRosterGroup'
        db.delete_table('ejddjango_sharedrostergroup_members')


    models = {
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
        'ejddjango.domain': {
            'Meta': {'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ejddjango.sharedrostergroup': {
            'Meta': {'object_name': 'SharedRosterGroup'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ejddjango.Domain']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ejddjango.UserJID']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site_group': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'srg'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.Group']"})
        },
        'ejddjango.userjid': {
            'Meta': {'unique_together': "(('node', 'domain'),)", 'object_name': 'UserJID'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jids'", 'to': "orm['ejddjango.Domain']"}),
            'node': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site_user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'jid'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['ejddjango']