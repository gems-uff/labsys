from django.contrib import admin

from .models import ObservedSymptom, Symptom


class SymptomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sintomas', {'fields': [
            'name',
            'is_primary',
        ]})
    ]


class ObservedSymptomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sintomas observados', {'fields': [
            'symptom',
            'observed',
            'details',
        ]})
    ]


admin.site.register(ObservedSymptom)
admin.site.register(Symptom, SymptomAdmin)