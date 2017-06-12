from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import ObservedSymptom, Symptom
from .forms import ObservedSymptomInlineFormset, ObservedSymptomFormSet


class ObservedSymptomInline(admin.TabularInline):
    model = ObservedSymptom
    formset = ObservedSymptomInlineFormset
    extra = 0
    #extra = len(Symptom.get_primary_symptoms_dict())
    #max_num = len(Symptom.get_primary_symptoms_dict())
    verbose_name_plural = 'Sintomas observados'
    # readonly_fields = ('symptom',)
    fieldsets = [
        ('Sintomas observados', {'fields': [
            'symptom',
            'observed',
            'details',
        ]}),
    ]


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

