from django.contrib import admin
from .models import Patient, PatientRegister, FluVaccine, Sample, CollectionType


class FluVaccineInline(admin.StackedInline):
    model = FluVaccine
    extra = 1


class SampleInline(admin.StackedInline):
    model = Sample
    extra = 1


class PatientRegisterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informações do Paciente', {'fields': ['patient']}),
        ('Dados institucionais', {'fields': ['id_gal_origin']}),
    ]
    inlines = [
        SampleInline,
        FluVaccineInline,
    ]


admin.site.register(Patient)
admin.site.register(Sample)
admin.site.register(CollectionType)
admin.site.register(PatientRegister, PatientRegisterAdmin)
