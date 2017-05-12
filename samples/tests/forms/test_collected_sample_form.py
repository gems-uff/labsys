import datetime

from django.test import TestCase

from samples.forms import CollectedSampleForm
from samples.models import (
    Patient, AdmissionNote, CollectedSample, CollectionType,
)


class CollectedSampleFormTest(TestCase):

    def setUp(self):
        patient = Patient(name="Collected Sample Form Patient")
        patient.save()
        self.admission_note = AdmissionNote.objects.create(
            patient=patient, id_gal_origin="1234567890")
        self.collection_type = CollectionType.objects.create(
            method_name="Método de coleta teste primário",
            is_primary=True,
        )
        self.other_collection_type = CollectionType.objects.create(
            method_name="Método de coleta teste secundário",
            is_primary=False,
        )

    def test_two_selected_methods_invalid(self):
        form = CollectedSampleForm({
            'collection_type': self.collection_type,
            'other_collection_type': self.other_collection_type,
            'collection_date': "30/12/2018",
        })
        self.assertFalse(form.is_valid())

