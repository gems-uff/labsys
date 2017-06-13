from django.contrib import admin

from collected_sample.models import CollectedSample
from symptoms.models import ObservedSymptom
from symptoms.admin import ObservedSymptomInline

from .models import AdmissionNote


class CollectedSampleInline(admin.StackedInline):
    model = CollectedSample
    extra = 1


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
    inlines = [CollectedSampleInline, ObservedSymptomInline]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)

