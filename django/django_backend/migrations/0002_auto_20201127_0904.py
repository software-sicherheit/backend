# Generated by Django 3.0.5 on 2020-11-27 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='id',
            new_name='_id',
        ),
    ]