from django.contrib import admin

from .models import Patient, Address


class ResidenceInline(admin.StackedInline):
    model = Address


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
    ]


admin.site.register(Patient, PatientAdmin)
