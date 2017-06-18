import datetime

from django.db import models

from labsys.custom import models as cmodels
from patients.models import Patient


class AdmissionNote(models.Model):
    id_request_gal = models.CharField(
        'Número da requisição (GAL)',
        max_length=30,
    )
    id_lvrs_intern = models.CharField(
        'Número interno (LVRS)',
        help_text='Número interno do laboratório, ex: 334/2017',
        max_length=30,
    )
    details = models.CharField(
        'Informações adicionais',
        help_text='Qualquer informação considerada relevante',
        max_length=1023,
        blank=True,
    )
    requester = models.CharField(
        'Instituto solicitante',
        max_length=255,
        help_text='LACEN ou instituto que solicitou o exame',
    )
    health_unit = models.CharField(
        'Unidade de saúde',
        max_length=255,
        help_text='unidade onde o paciente foi avaliado',
    )
    state = models.CharField('Estado', max_length=2)
    city = models.CharField('Município', max_length=255)
    admission_date = models.DateField(
        'Data de entrada (LVRS)',
        help_text='quando a amostra chegou no LVRS',
        null=True,
        blank=True,
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Número interno: {}".format(self.id_lvrs_intern)


class ISimpleDatedEvent(models.Model):
    class Meta:
        abstract = True

    occurred = models.NullBooleanField()
    date = models.DateField(
        null=True,
        blank=True,
    )
    admission_note = models.OneToOneField(
        AdmissionNote,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if self.occurred is None:
            return
        else:
            super(ISimpleDatedEvent, self).save(*args, **kwargs)


class FluVaccine(ISimpleDatedEvent):
    pass


class ClinicalEvolution(ISimpleDatedEvent):
    pass


class Hospitalization(ISimpleDatedEvent):
    pass


class UTIHospitalization(ISimpleDatedEvent):
    pass
