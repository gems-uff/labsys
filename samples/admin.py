from django.contrib import admin
from .models import Patient, PatientRegister, FluVaccine


class PatientInline(admin.TabularInline):
    model = Patient
    extra = 0


class FluVaccineInline(admin.StackedInline):
    model = FluVaccine
    extra = 1


class PatientRegisterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informações do Paciente', {'fields': ['patient']}),
        ('Dados institucionais', {'fields': ['id_gal_origin']}),
    ]
    inlines = [FluVaccineInline]


admin.site.register(Patient)
admin.site.register(PatientRegister, PatientRegisterAdmin)