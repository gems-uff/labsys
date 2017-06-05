from django.db import models

from admission_notes.models import AdmissionNote


class CollectionMethod(models.Model):
    method_name = models.CharField(
        'Método de coleta',
        max_length=255,
    )
    is_primary = models.BooleanField(
        verbose_name='Principal?',
        default=False,
    )

    def __str__(self):
        return self.method_name


class CollectedSample(models.Model):
    collection_date = models.DateField(
        'Data de coleta',
        null=True,
        blank=True,
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
    )
    collection_type = models.ForeignKey(
        CollectionMethod,
        verbose_name='Método de coleta',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Amostra coletada"