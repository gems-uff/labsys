from django.db import models


class Patient(models.Model):
    name = models.CharField(
        verbose_name="Nome do paciente",
        max_length=255,
    )

    def __str__(self):
        return self.name


class PatientRegister(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
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
    was_applied = models.NullBooleanField(
        verbose_name="Recebeu vacina contra gripe?"
    )
    patient_register = models.OneToOneField(
        PatientRegister,
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


class Sample(models.Model):
    collection_date = models.DateField(
        verbose_name="Data de coleta",
    )
    patient_register = models.ForeignKey(
        PatientRegister,
    )
    collection_type = models.ForeignKey(
        CollectionType,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return "Amostra"


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
    patient_register = models.ForeignKey(
        PatientRegister,
        on_delete=models.CASCADE,
    )
    observed = models.NullBooleanField(
        verbose_name="Apresenta sintoma?",
        default=None,
    )

    def __str__(self):
        return "Sintoma apresentado"
