# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0002_auto_20170424_1731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fluvaccine',
            old_name='patient',
            new_name='patient_register',
        ),
    ]