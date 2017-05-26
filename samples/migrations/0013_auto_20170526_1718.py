# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0012_auto_20170512_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectedsample',
            name='collection_date',
            field=models.DateField(null=True, verbose_name='Data de coleta'),
        ),
        migrations.AlterField(
            model_name='collectedsample',
            name='collection_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='samples.CollectionType', verbose_name='Método de coleta'),
        ),
    ]
