from django.contrib import admin

from .models import CollectedSample, CollectionMethod


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
            'collection_type',
        ]})
    ]


admin.site.register(CollectedSample)
admin.site.register(CollectionMethod, CollectionMethodAdmin)
