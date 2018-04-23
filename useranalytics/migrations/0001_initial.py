# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('client_name', models.CharField(unique=True, max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('api_key', models.CharField(null=True, db_index=True, blank=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('page_name', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(null=True)),
                ('client', models.ForeignKey(to='useranalytics.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SessionInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sessionkey', models.CharField(null=True, blank=True, max_length=32)),
                ('login_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(null=True, blank=True, max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='clientdata',
            name='location',
            field=models.ForeignKey(to='useranalytics.Location'),
        ),
        migrations.AddField(
            model_name='clientdata',
            name='session',
            field=models.ForeignKey(to='useranalytics.SessionInfo'),
        ),
        migrations.AddField(
            model_name='clientdata',
            name='user',
            field=models.ForeignKey(to='useranalytics.UserInfo'),
        ),
    ]
