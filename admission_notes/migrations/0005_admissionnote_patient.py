# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 02:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_auto_20170603_2329'),
        ('admission_notes', '0004_auto_20170603_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionnote',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patients.Patient'),
        ),
    ]
