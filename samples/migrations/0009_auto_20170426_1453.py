# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0008_patientregister_observed_symptoms'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectedSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_date', models.DateField(verbose_name='Data de coleta')),
            ],
        ),
        migrations.RenameModel(
            old_name='PatientRegister',
            new_name='AdmissionNote',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='collection_type',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='patient_register',
        ),
        migrations.RenameField(
            model_name='fluvaccine',
            old_name='patient_register',
            new_name='admission_note',
        ),
        migrations.RenameField(
            model_name='observedsymptom',
            old_name='patient_register',
            new_name='admission_note',
        ),
        migrations.AlterUniqueTogether(
            name='observedsymptom',
            unique_together=set([('symptom', 'admission_note')]),
        ),
        migrations.DeleteModel(
            name='Sample',
        ),
        migrations.AddField(
            model_name='collectedsample',
            name='admission_note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samples.AdmissionNote'),
        ),
        migrations.AddField(
            model_name='collectedsample',
            name='collection_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='samples.CollectionType'),
        ),
    ]
