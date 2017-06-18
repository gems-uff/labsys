from django.contrib import admin

from .models import ObservedSymptom, Symptom


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sintomas', {'fields': [
            'name',
            'is_primary',
        ]})
    ]


@admin.register(ObservedSymptom)
class ObservedSymptomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sintomas observados', {'fields': [
            'symptom',
            'admission_note',
            'observed',
            'details',
        ]})
    ]

