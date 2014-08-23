# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bill.currency'
        db.add_column('bridgebill_bill', 'currency',
                      self.gf('django.db.models.fields.CharField')(default='S$', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bill.currency'
        db.delete_column('bridgebill_bill', 'currency')


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
        'bridgebill.bill': {
            'Meta': {'object_name': 'Bill'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bridgebill.UserProfile']"}),
            'overall_bill_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'bridgebill.billdetails': {
            'Meta': {'object_name': 'BillDetails'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bridgebill.Bill']"}),
            'bill_cleared': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bill_cleared_date': ('django.db.models.fields.DateField', [], {}),
            'bill_deleted': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'billdetail_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'borrower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bridgebill.UserFriend']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'individual_bill_created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'bridgebill.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'})
        },
        'bridgebill.userfriend': {
            'Meta': {'object_name': 'UserFriend'},
            'friend_created_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'friend_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'friend_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bridgebill.UserProfile']"}),
            'userfriend_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'bridgebill.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'userprofile_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bridgebill']