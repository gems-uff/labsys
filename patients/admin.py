from django.contrib import admin

from .models import Patient, Locality

class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados do paciente', {'fields': [
            'name',
            'birth_date',
            'age_in_hours',
            'gender',
            'pregnant',
        ]}),
        ('Endereço de residência', {'fields': ['residence']}),
    ]


admin.site.register(Locality)
admin.site.register(Patient, PatientAdmin)
