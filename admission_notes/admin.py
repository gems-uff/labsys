from django.contrib import admin

from .models import AdmissionNote, Patient


class AdmissionNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados institucionais', {'fields': [
            'id_gal',
            'requester',
            'health_unit',
            'state',
            'city',
            'admission_date',
        ]}),
    ]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)
