# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-11 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symptoms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nome do sintoma'),
        ),
    ]