# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-11 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission_notes', '0006_auto_20170605_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionnote',
            name='details',
            field=models.CharField(default='', max_length=1023, verbose_name='Informações adicionais'),
            preserve_default=False,
        ),
    ]
