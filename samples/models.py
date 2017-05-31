from django.db import models

from samples.custom import models as cmodels


class Patient(models.Model):
    name = models.CharField(
        verbose_name="Nome do paciente",
        max_length=255,
    )

    def __str__(self):
        return self.name


class AdmissionNote(models.Model):
    patient = models.ForeignKey(
        Patient,
        null=True,
    )
    observed_symptoms = models.ManyToManyField(
        'Symptom',
        through='ObservedSymptom',
    )
    id_gal_origin = models.CharField(
        verbose_name="ID Gal Origem",
        max_length=255,
    )

    def __str__(self):
        return "ID Gal: {}".format(self.id_gal_origin)


class FluVaccine(models.Model):
    was_applied = cmodels.YesNoIgnoredField(
        verbose_name="Recebeu vacina contra gripe?",
    )
    date_applied = models.DateField(
        verbose_name="Data de aplicação",
        null=True,
        blank=True,
    )
    admission_note = models.OneToOneField(
        AdmissionNote,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Vacina contra gripe"


class CollectionType(models.Model):
    method_name = models.CharField(
        verbose_name="Método de coleta",
        max_length=255,
    )
    is_primary = models.BooleanField(
        verbose_name="Principal?",
        default=True,
    )

    def __str__(self):
        return self.method_name


class CollectedSample(models.Model):
    collection_date = models.DateField(
        verbose_name="Data de coleta",
        null=True,
        blank=False,
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
    )
    collection_type = models.ForeignKey(
        CollectionType,
        verbose_name="Método de coleta",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    def __str__(self):
        return "Amostra coletada"


class Symptom(models.Model):
    name = models.CharField(
        verbose_name="Nome do sintoma",
        max_length=255,
    )
    is_primary = models.BooleanField(
        verbose_name="Principal?",
        default=True,
    )

    def __str__(self):
        return self.name


class ObservedSymptom(models.Model):
    symptom = models.ForeignKey(
        Symptom,
        on_delete=models.CASCADE,
        verbose_name="Sintoma principal"
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
        on_delete=models.CASCADE,
    )
    observed = cmodels.YesNoIgnoredField(
        verbose_name="Apresenta sintoma?",
        default=None,
    )

    class Meta:
        unique_together = (
            ('symptom', 'admission_note'),
        )

    @classmethod
    def get_primary_symptoms_dict(cls):
        primary_symptoms = [
            {'symptom': symptom.name}
            for symptom in Symptom.objects.all() if symptom.is_primary
        ]
        return primary_symptoms

    def __str__(self):
        if self.symptom is not None:
            return self.symptom.name
        else:
            return "Sintoma apresentado"
