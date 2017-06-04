from django.contrib import admin

from .models import (
    Patient,
    AdmissionNote,
    FluVaccine,
    CollectedSample, CollectionType,
    Symptom, ObservedSymptom
)


class FluVaccineInline(admin.StackedInline):
    model = FluVaccine
    extra = 1


class CollectedSampleInline(admin.StackedInline):
    model = CollectedSample
    extra = 1


class ObservedSymptomInline(admin.StackedInline):
    model = ObservedSymptom
    extra = 1


class AdmissionNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informações do Paciente', {'fields': ['patient']}),
        ('Dados institucionais', {'fields': ['id_gal_origin']}),
    ]
    inlines = [
        CollectedSampleInline,
        FluVaccineInline,
        ObservedSymptomInline,
    ]


#admin.site.register(Patient)
#admin.site.register(AdmissionNote, AdmissionNoteAdmin)
#admin.site.register(CollectedSample)
#admin.site.register(CollectionType)
#admin.site.register(Symptom)
