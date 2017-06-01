from django.contrib import admin

from .models import AdmissionNote


class AdmissionNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados institucionais', {'fields': [
            'id_gal',
            'requestor',
            'health_unit',
            'state',
            'city',
        ]}),
    ]

admin.site.register(AdmissionNote, AdmissionNoteAdmin)
