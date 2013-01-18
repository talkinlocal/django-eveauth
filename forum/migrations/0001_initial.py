# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForumProfile'
        db.create_table('forum_forumprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_profile', unique=True, to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('avatar', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('topics_per_page', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('posts_per_page', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('auto_fast_reply', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('post_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('forum', ['ForumProfile'])

        # Adding model 'Section'
        db.create_table('forum_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('forum', ['Section'])

        # Adding model 'Forum'
        db.create_table('forum_forum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forums', to=orm['forum.Section'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('topic_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_post_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('last_topic_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('last_user_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('last_username', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('forum', ['Forum'])

        # Adding model 'Topic'
        db.create_table('forum_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topics', to=orm['forum.Forum'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topics', to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('pinned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('post_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('metapost_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_post_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_user_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('last_username', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('forum', ['Topic'])

        # Adding model 'Post'
        db.create_table('forum_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['forum.Topic'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
            ('posted_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('edited_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('emoticons', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('num_in_topic', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('forum', ['Post'])

        # Adding model 'Search'
        db.create_table('forum_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='searches', to=orm['auth.User'])),
            ('searched_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('criteria_json', self.gf('django.db.models.fields.TextField')()),
            ('result_ids', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('forum', ['Search'])


    def backwards(self, orm):
        # Deleting model 'ForumProfile'
        db.delete_table('forum_forumprofile')

        # Deleting model 'Section'
        db.delete_table('forum_section')

        # Deleting model 'Forum'
        db.delete_table('forum_forum')

        # Deleting model 'Topic'
        db.delete_table('forum_topic')

        # Deleting model 'Post'
        db.delete_table('forum_post')

        # Deleting model 'Search'
        db.delete_table('forum_search')


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
        'eveauth.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'corp_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'forum.forum': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Forum'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_topic_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_user_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forums'", 'to': "orm['forum.Section']"}),
            'topic_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'forum.forumprofile': {
            'Meta': {'ordering': "('user',)", 'object_name': 'ForumProfile'},
            'auto_fast_reply': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'posts_per_page': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'topics_per_page': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'forum.post': {
            'Meta': {'ordering': "('-posted_at', '-id')", 'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'edited_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'emoticons': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_in_topic': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'posted_at': ('django.db.models.fields.DateTimeField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['forum.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['auth.User']"}),
            'user_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'forum.search': {
            'Meta': {'ordering': "('-searched_at',)", 'object_name': 'Search'},
            'criteria_json': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_ids': ('django.db.models.fields.TextField', [], {}),
            'searched_at': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'searches'", 'to': "orm['auth.User']"})
        },
        'forum.section': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'forum.topic': {
            'Meta': {'ordering': "('-last_post_at', '-started_at')", 'object_name': 'Topic'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': "orm['forum.Forum']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_user_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'metapost_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pinned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['forum']
