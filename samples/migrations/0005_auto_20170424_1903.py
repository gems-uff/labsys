# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0004_sample'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_name', models.CharField(max_length=255, verbose_name='Método de coleta')),
                ('is_primary', models.BooleanField(default=True, verbose_name='Principal?')),
            ],
        ),
        migrations.AlterField(
            model_name='fluvaccine',
            name='was_applied',
            field=models.NullBooleanField(verbose_name='Recebeu vacina contra gripe?'),
        ),
        migrations.AddField(
            model_name='sample',
            name='collection_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='samples.CollectionType'),
        ),
    ]