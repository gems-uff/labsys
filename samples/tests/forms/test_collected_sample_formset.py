from django.test import TestCase
from django.core.urlresolvers import reverse

from samples.forms import CollectedSampleForm, AdmissionNoteForm
from samples.models import (
    Patient, AdmissionNote, CollectedSample, CollectionType,
)


class CollectedSampleFormSetTest(TestCase):
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
        
    """
    TODO: Edge cases
    - Formulário com 1 amostra (salvar no DB)
    - Formulário com 2 amostras (salvar no DB)
    - Formulário com 1 amostra e 1 vazia
    - Formulário com 1 amostra e 1 parcialmente vazia
    
    """
