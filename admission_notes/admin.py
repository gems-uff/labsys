from django.contrib import admin

from collected_sample.models import CollectedSample

from .models import AdmissionNote


class CollectedSampleInline(admin.StackedInline):
    model = CollectedSample
    extra = 1


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
    inlines = [CollectedSampleInline]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)

