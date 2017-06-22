# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-22 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission_notes', '0012_auto_20170618_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionnote',
            name='first_symptoms_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data dos primeiros sintomas'),
        ),
        migrations.AddField(
            model_name='admissionnote',
            name='semepi',
            field=models.PositiveIntegerField(blank=True, help_text='Calendário epidemiológico disponível em:             http://portalsinan.saude.gov.br/calendario-epidemiologico-2017', null=True, verbose_name='Semana epidemiológica'),
        ),
    ]
