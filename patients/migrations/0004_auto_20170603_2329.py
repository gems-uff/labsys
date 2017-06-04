# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 02:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_auto_20170603_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.IntegerField(choices=[(1, 'Brasil'), (2, 'Outros')], default=1, verbose_name='País')),
                ('state', models.CharField(max_length=2, verbose_name='Estado UF')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='Município')),
                ('neighborhood', models.CharField(blank=True, max_length=255, verbose_name='Bairro')),
                ('zone', models.IntegerField(choices=[(1, 'Urbana'), (2, 'Rural'), (3, 'Periurbana'), (9, 'Ignorado')], default=9, verbose_name='Zona')),
            ],
        ),
        migrations.RemoveField(
            model_name='patient',
            name='residence',
        ),
        migrations.DeleteModel(
            name='Locality',
        ),
        migrations.AddField(
            model_name='address',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='residence', to='patients.Patient'),
        ),
    ]
