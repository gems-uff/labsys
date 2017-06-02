import datetime

#from labsys.patients import Patient

from django.db import models

class AdmissionNote(models.Model):
    id_gal = models.CharField(max_length=30)
    requester = models.CharField(max_length=255)
    health_unit = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=255)

    def __str__(self):
        return "ID Gal: {}".format(self.id_gal)
