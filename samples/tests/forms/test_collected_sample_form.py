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
            patient=patient, id_gal_origin="1234567890"
        )
        self.other_collection_type = CollectionType.objects.create(
            method_name="Other collection type",
            is_primary=False,
        )
        self.collection_type = CollectionType.objects.create(
            method_name="Primary collection type",
            is_primary=True,
        )

    def test_valid_form_primary(self):
        form = CollectedSampleForm({
            'collection_type': CollectionType.objects.filter(id=self.collection_type.id),
            'collection_date': "30/12/2018",
        })
        self.assertTrue(form.is_valid())
        collected_sample = form.save_fk(self.admission_note)
        self.assertEquals(collected_sample.collection_type, self.collection_type)
        self.assertEquals(collected_sample.collection_date, datetime.date(2018, 12, 30))

    def test_valid_form_secondary(self):
        form = CollectedSampleForm({
            'other_collection_type': CollectionType.objects.filter(id=self.other_collection_type.id),
            'collection_date': "30/12/2018",
        })
        self.assertTrue(form.is_valid())

    def test_save_other_collection_in_instance(self):
        form = CollectedSampleForm({
            'other_collection_type': CollectionType.objects.filter(id=self.other_collection_type.id),
            'collection_date': "30/12/2018",
        })
        self.assertTrue(form.is_valid())
        collected_sample = form.save_fk(self.admission_note)
        self.assertEquals(collected_sample.admission_note, self.admission_note)
        self.assertEquals(collected_sample.collection_type, self.other_collection_type)

    def test_two_selected_methods(self):
        form = CollectedSampleForm({
            'collection_type': CollectionType.objects.filter(id=self.collection_type.id),
            'other_collection_type': CollectionType.objects.filter(id=self.other_collection_type.id),
            'collection_date': "30/12/2018",
        })
        self.assertIn("Selecionar somente um método de coleta", form.errors['__all__'])
        self.assertFalse(form.is_valid())

    def test_no_selected_method(self):
        form = CollectedSampleForm({
            'collection_date': "30/12/2018",
        })
        self.assertIn("Selecionar pelo menos um método de coleta", form.errors['__all__'])
        self.assertFalse(form.is_valid())

    def test_invalid_date_format(self):
        form = CollectedSampleForm({
            'collection_type': CollectionType.objects.filter(id=self.collection_type.id),
            'collection_date': "300/12/2018",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Informe uma data válida.", form.errors['collection_date'])
