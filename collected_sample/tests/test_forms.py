import datetime

from django.test import TestCase

from collected_sample.forms import CollectedSampleForm
from collected_sample.models import CollectedSample, CollectionMethod
from patients.models import Patient
from admission_notes.models import AdmissionNote
import admission_notes.utils as utils


class CollectedSampleFormTest(TestCase):

    def setUp(self):
        self.admission_note = AdmissionNote.objects.create(
            **utils.get_admission_note(dict=True)
        )
        self.other_collection_method = CollectionMethod.objects.create(
            name='Other collection method',
            is_primary=False,
        )
        self.collection_method = CollectionMethod.objects.create(
            name='Primary collection method',
            is_primary=True,
        )
        self.collection_date = '30/12/2018'

        self.valid_form_primary_method = CollectedSampleForm({
            'collection_method': CollectionMethod.objects.filter(
                id=self.collection_method.id),
            'collection_date': self.collection_date,
        })
        self.valid_form_other_method = CollectedSampleForm({
            'other_collection_method': CollectionMethod.objects.filter(
                id=self.other_collection_method.id),
            'collection_date': self.collection_date,
        })

    def test_valid_form_primary_method(self):
        form = self.valid_form_primary_method
        self.assertTrue(form.is_valid())

    def test_valid_form_other_method(self):
        form = self.valid_form_other_method
        self.assertTrue(form.is_valid())

    def test_form_instance_creation_primary_method(self):
        form = self.valid_form_primary_method
        collected_sample = form.save(self.admission_note)
        self.assertEquals(
            collected_sample.collection_method, self.collection_method)
        self.assertEquals(
            collected_sample.collection_date, datetime.date(2018, 12, 30))

    def test_form_instance_creation_other_method(self):
        form = self.valid_form_other_method
        collected_sample = form.save(self.admission_note)
        self.assertEquals(
            collected_sample.collection_method, self.other_collection_method)
        self.assertEquals(
            collected_sample.collection_date, datetime.date(2018, 12, 30))

    def test_two_selected_collection_methods(self):
        form = CollectedSampleForm({
            'collection_method': CollectionMethod.objects.filter(
                id=self.collection_method.id),
            'other_collection_method': CollectionMethod.objects.filter(
                id=self.other_collection_method.id),
            'collection_date': '300/12/2012',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Selecionar somente um método de coleta', form.errors['__all__'])

    def test_no_selected_collection_method(self):
        form = CollectedSampleForm({
            'collection_date': self.collection_date,
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Selecionar pelo menos um método de coleta', form.errors['__all__'])

    def test_invalid_date_format(self):
        form = CollectedSampleForm({
            'collection_method': CollectionMethod.objects.filter(
                id=self.collection_method.id),
            'collection_date': '300/12/2012',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Informe uma data válida.", form.errors['collection_date'])


'''
class CollectedSampleFormSetTest(TestCase):
    def setUp(self):
        patient = Patient(name="Collected Sample Form Patient")
        patient.save()
        self.admission_note = AdmissionNote.objects.create(
            patient=patient, id_gal_origin="1234567890"
        )
        self.other_collection_method = CollectionMethod.objects.create(
            method_name="Other collection method",
            is_primary=False,
        )
        self.collection_method = CollectionMethod.objects.create(
            method_name="Primary collection method",
            is_primary=True,
        )
'''

"""
TODO: Edge cases
- Formulário com 1 amostra (salvar no DB)
- Formulário com 2 amostras (salvar no DB)
- Formulário com 1 amostra e 1 vazia
- Formulário com 1 amostra e 1 parcialmente vazia

"""