# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collected_sample', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectionmethod',
            name='method_name',
        ),
        migrations.AddField(
            model_name='collectedsample',
            name='details',
            field=models.CharField(blank=True, max_length=255, verbose_name='Informações adicionais'),
        ),
        migrations.AddField(
            model_name='collectionmethod',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Nome do método de coleta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collectionmethod',
            name='is_primary',
            field=models.BooleanField(default=False, verbose_name='Método principal?'),
        ),
    ]
