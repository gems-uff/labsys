import datetime

#from labsys.patients import Patient

from django.db import models

class AdmissionNote(models.Model):
    id_gal = models.CharField(max_length=30)
    requester = models.CharField(
        max_length=255,
        help_text="LACEN ou instituto que solicitou o exame",
    )
    health_unit = models.CharField(
        max_length=255,
        help_text="unidade onde o paciente foi avaliado",
    )
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    admission_date = models.DateField(
        verbose_name="Data de entrada (LVRS)",
        help_text="quando a amostra chegou no LVRS",
        null=True,
        blank=True,
    )

    def __str__(self):
        return "ID Gal: {}".format(self.id_gal)
