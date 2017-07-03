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
        max_length=500,
        blank=True,
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
    )

    def __str__(self):
        return "Amostra coletada em {}".format(self.collection_date)


class RTPCR_CDC(models.Model):
    sample = models.ForeignKey(CollectedSample)

    flu_type = models.IntegerField(
        verbose_name='Resultado Tipagem',
        choices=(
            (1, 'A - Flu A'),
            (2, 'B - Flu B'),
            (3, 'Não realizado'),
            (4, 'Inconclusivo'),
            (9, 'Ignorado'),
        ),
        default=9,
    )
    flu_subtype = models.IntegerField(
        verbose_name='Subtipo ou Linhagem',
        choices=(
            (1, 'H1'),
            (2, 'H3'),
            (3, 'Yamagata'),
            (4, 'Victoria'),
            (5, 'Não realizado'),
            (6, 'Não subtipável'),
            (9, 'Ignorado'),
        ),
        default=9,
    )

    details = models.CharField(
        max_length=255,
        blank=True,
    )

