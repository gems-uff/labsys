from django.contrib import admin

import nested_admin

from .models import Patient, Locality
from admission_notes.models import AdmissionNote


class AdmissionNoteInline(admin.StackedInline):
    model = AdmissionNote
    max_num = 1
    extra = 1


class LocalityAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Localidade', {'fields': [
            'country',
            'state',
            'city',
            'neighborhood',
            'zone',
        ]})
    ]


class PatientAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        ('Dados do paciente', {'fields': [
            'name',
            'birth_date',
            'age_in_hours',
            'gender',
            'pregnant',
            'residence',
        ]}),
    ]


admin.site.register(Patient, PatientAdmin)
admin.site.register(Locality, LocalityAdmin)
