# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission_notes', '0007_admissionnote_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionnote',
            name='city',
            field=models.CharField(max_length=255, verbose_name='Município'),
        ),
        migrations.AlterField(
            model_name='admissionnote',
            name='details',
            field=models.CharField(blank=True, help_text='Qualquer informação considerada relevante', max_length=1023, verbose_name='Informações adicionais'),
        ),
        migrations.AlterField(
            model_name='admissionnote',
            name='state',
            field=models.CharField(max_length=2, verbose_name='Estado'),
        ),
    ]
