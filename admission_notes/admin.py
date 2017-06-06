from django.contrib import admin

from collected_sample.models import CollectedSample
from symptoms.models import ObservedSymptom

from .models import AdmissionNote


class CollectedSampleInline(admin.StackedInline):
    model = CollectedSample
    extra = 1

class ObservedSymptomInline(admin.TabularInline):
    model = ObservedSymptom


class AdmissionNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados institucionais', {'fields': [
            'id_gal',
            'requester',
            'health_unit',
            'state',
            'city',
            'admission_date',
            'patient',
        ]}),
    ]
    inlines = [CollectedSampleInline, ObservedSymptomInline]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)

