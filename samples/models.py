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
    id_gal_origin = models.CharField(
        verbose_name="ID Gal Origem",
        max_length=255,
    )

    def __str__(self):
        return "ID Gal: {}".format(self.id_gal_origin)


class FluVaccine(models.Model):
    was_applied = models.NullBooleanField(
        verbose_name="Recebeu vacina contra gripe"
    )
    patient_register = models.OneToOneField(
        PatientRegister,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Vacina contra gripe"


class Sample(models.Model):
    collection_date = models.DateField(
        verbose_name="Data de coleta",
    )
    patient_register = models.ForeignKey(
        PatientRegister,
    )

    def __str__(self):
        return "Amostra"
