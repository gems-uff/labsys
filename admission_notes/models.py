
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
    first_symptoms_date = models.DateField(
        'Data dos primeiros sintomas',
        null=True,
        blank=True,
    )
    semepi = models.PositiveIntegerField(
        'Semana epidemiológica',
        help_text='Calendário epidemiológico disponível em: \
            http://portalsinan.saude.gov.br/calendario-epidemiologico-2017',
        blank=True,
        null=True,
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



class AntiviralUse(models.Model):
    antiviral = models.IntegerField(
        verbose_name='Selecione',
        help_text='Caso \"outro\", informar',
        choices=(
            (1, "1 - Não usou"),
            (2, "2 - Oseltamivir"),
            (3, "3 - Zanamivir"),
            (4, "4 - Outro, especifique"),
            (9, "9 - Ignorado"),
        ),
        default=9,
    )
    date = models.DateField(
        'Data de uso',
        help_text='Data do início do tratamento com antiviral',
        null=True,
        blank=True,
    )
    details = models.CharField(
        'Informações adicionais',
        help_text='Ex.: outro antiviral',
        max_length=255,
        blank=True,
    )
    admission_note = models.OneToOneField(
        AdmissionNote,
        on_delete=models.CASCADE,
    )


class XRayExam(models.Model):
    xray = models.IntegerField(
        verbose_name='Selecione',
        help_text='mais sugestiva para diagnóstico de SRAG',
        choices=(
            (1, "1 - Normal"),
            (2, "2 - Infiltrado intersticial"),
            (3, "3 - Consolidação"),
            (4, "4 - Misto"),
            (5, "5 - Outro, especifique"),
            (6, "6 - Não realizado"),
            (9, "9 - Ignorado"),
        ),
        default=9,
    )
    date = models.DateField(
        'Data de realização do exame',
        null=True,
        blank=True,
    )
    details = models.CharField(
        'Informações adicionais',
        help_text='Ex.: outro tipo de Raio-X',
        max_length=255,
        blank=True,
    )
    admission_note = models.OneToOneField(
        AdmissionNote,
        on_delete=models.CASCADE,
    )
