# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 14:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apprest', '0006_auto_20161210_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='hora',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 11, 14, 17, 32, 478594)),
        ),
    ]