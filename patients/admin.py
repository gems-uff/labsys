from django.contrib import admin

from .models import Patient, Address
from admission_notes.models import AdmissionNote


class ResidenceInline(admin.StackedInline):
    model = Address


class AdmissionNoteInline(admin.StackedInline):
    model = AdmissionNote
    max_num = 1
    extra = 1



class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados do paciente', {'fields': [
            'name',
            'birth_date',
            'age_in_hours',
            'gender',
            'pregnant',
        ]}),
    ]
    inlines = [
        ResidenceInline,
        AdmissionNoteInline,
    ]


admin.site.register(Patient, PatientAdmin)
