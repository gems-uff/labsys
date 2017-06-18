from django.contrib import admin

from collected_sample.models import CollectedSample
from symptoms.models import ObservedSymptom

from .models import (
    AdmissionNote, FluVaccine, ClinicalEvolution,
    Hospitalization, UTIHospitalization,
)


class FluVaccineInline(admin.TabularInline):
    model = FluVaccine


class ClinicalEvolutionInline(admin.TabularInline):
    model = ClinicalEvolution


class HospitalizationInline(admin.TabularInline):
    model = Hospitalization


class UTIHospitalizationInline(admin.TabularInline):
    model = UTIHospitalization


class CollectedSampleInline(admin.StackedInline):
    model = CollectedSample
    extra = 0


class ObservedSymptomInline(admin.TabularInline):
    model = ObservedSymptom
    extra = 0
    verbose_name_plural = 'Sintomas observados'
    fieldsets = [
        ('Sintomas observados', {'fields': [
            'symptom',
            'observed',
            'details',
        ]}),
    ]


class AdmissionNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados institucionais', {'fields': [
            'id_request_gal',
            'id_lvrs_intern',
            'requester',
            'health_unit',
            'state',
            'city',
            'admission_date',
        ]}),
        ('Dados do paciente', {'fields': [
            'patient',
        ]})
    ]
    inlines = [
        CollectedSampleInline,
        ObservedSymptomInline,
        FluVaccineInline,
        ClinicalEvolutionInline,
        HospitalizationInline,
        UTIHospitalizationInline,
    ]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)

