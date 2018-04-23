# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useranalytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessioninfo',
            name='logout_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='client',
            field=models.ForeignKey(to='useranalytics.Client', null=True),
        ),
    ]
