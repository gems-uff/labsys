from django.contrib import admin

from .models import CollectedSample, CollectionMethod, RSVExam, RTPCRExam


class RSVExamInline(admin.TabularInline):
    model = RSVExam
    extra = 0
    fieldsets = [
        ('Exame de RSV', {'fields': [
            'details',
            'performed_inhouse',
        ]}),
    ]


class RTPCRExamInline(admin.TabularInline):
    model = RTPCRExam
    extra = 0
    fieldsets = [
        ('Exame de RTPCR', {'fields': [
            'details',
            'performed_inhouse',
        ]}),
    ]


class CollectionMethodAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Métodos de coleta', {'fields': [
            'name',
            'is_primary',
        ]})
    ]


class CollectedSampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Amostra coletada', {'fields': [
            'collection_date',
            'collection_method',
            'details',
            'admission_note',
        ]})
    ]
    inlines = [RSVExamInline, RTPCRExamInline]


admin.site.register(RSVExam)
admin.site.register(RTPCRExam)
admin.site.register(CollectedSample, CollectedSampleAdmin)
admin.site.register(CollectionMethod, CollectionMethodAdmin)
