from django.db import models


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
    was_applied = models.NullBooleanField(
        verbose_name="Recebeu vacina contra gripe?"
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
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
    )
    collection_type = models.ForeignKey(
        CollectionType,
        on_delete=models.SET_NULL,
        null=True,
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
    )
    admission_note = models.ForeignKey(
        AdmissionNote,
        on_delete=models.CASCADE,
    )
    observed = models.NullBooleanField(
        verbose_name="Apresenta sintoma?",
        default=None,
    )

    class Meta:
        unique_together = (
            ('symptom', 'admission_note'),
        )

    def __str__(self):
        return "Sintoma apresentado"
