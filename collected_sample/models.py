from django.db import models

from admission_notes.models import AdmissionNote


class CollectionMethod(models.Model):
    name = models.CharField(
        'Nome do método de coleta',
        max_length=255,
        unique=True,
    )
    is_primary = models.BooleanField(
        'Método principal?',
        default=False,
    )

    def __str__(self):
        return self.name


class CollectedSample(models.Model):
    collection_date = models.DateField(
        'Data de coleta',
    )
    collection_method = models.ForeignKey(
        CollectionMethod,
        verbose_name='Método de coleta',
        on_delete=models.SET_NULL,
        null=True,
    )
    details = models.CharField(
        'Informações adicionais',
        max_length=255,
        blank=True,
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
    )

    def __str__(self):
        return "Amostra coletada em {}".format(self.collection_date)


class RSVExam(models.Model):
    details = models.CharField(
        'Placeholder RSV',
        max_length=255,
        blank=True,
    )
    performed_inhouse = models.BooleanField(
        'Realizado na FIOCRUZ/LVRS?',
        default=True,
    )
    sample = models.ForeignKey(
        CollectedSample,
    )


class RTPCRExam(models.Model):
    details = models.CharField(
        'Placeholder RTPCR',
        max_length=255,
        blank=True,
    )
    performed_inhouse = models.BooleanField(
        'Realizado na FIOCRUZ/LVRS?',
        default=True,
    )
    sample = models.ForeignKey(
        CollectedSample,
    )
