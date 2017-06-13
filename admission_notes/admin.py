from django.contrib import admin

import nested_admin

from collected_sample.models import CollectedSample
from symptoms.models import ObservedSymptom
from symptoms.admin import ObservedSymptomInline
from patients.models import Patient

from .models import AdmissionNote


class PatientInline(nested_admin.NestedTabularInline):
    model = Patient
    extra = 1

class CollectedSampleInline(admin.TabularInline):
    model = CollectedSample
    extra = 1


class AdmissionNoteAdmin(nested_admin.NestedModelAdmin):
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
        PatientInline,
    ]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)

