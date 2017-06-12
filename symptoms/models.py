from django.db import models

from labsys.custom import models as cmodels

from admission_notes.models import AdmissionNote


class Symptom(models.Model):
    name = models.CharField(
        'Nome do sintoma',
        max_length=255,
        unique=True,
    )
    is_primary = models.BooleanField(
        'Sintoma principal?',
        default=False,
    )

    @classmethod
    def get_primary_symptoms_dict(cls):
        primary_symptoms = [
            {'symptom': symptom}
            for symptom in cls.objects.all() if symptom.is_primary
        ]
        return primary_symptoms

    def __str__(self):
        return self.name


class ObservedSymptom(models.Model):
    symptom = models.ForeignKey(
        Symptom,
        on_delete=models.CASCADE,
        verbose_name='Sintoma',
    )
    observed = cmodels.YesNoIgnoredField(
        'Apresenta o sintoma?',
        default=None,
    )
    details = models.CharField(
        'Informações adicionais',
        max_length=255,
        blank=True,
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
        on_delete=models.CASCADE,
        verbose_name='Nota de admissão',
    )

    class Meta:
        unique_together = (
            ('symptom', 'admission_note'),
        )

    def __str__(self):
        if self.symptom is not None:
            return self.symptom.name
        else:
            return "Sintoma apresentado"