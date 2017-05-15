import datetime

from django.test import TestCase

from samples.forms import FluVaccineForm, AdmissionNoteForm, PatientForm
from samples.models import AdmissionNote, Patient


class FluVaccineFormTest(TestCase):

    def setUp(self):
        patient = Patient(name="Gabriel Test")
        patient.save()
        self.admission_note = AdmissionNote.objects.create(
            patient=patient, id_gal_origin="1234567890")

    def test_valid_data_vaccine_applied(self):
        form = FluVaccineForm({
            'was_applied': True,
            'date_applied': "30/12/2017",
        })
        self.assertTrue(form.is_valid())
        flu_vaccine = form.save_fk(self.admission_note)
        self.assertEqual(flu_vaccine.was_applied, True)
        self.assertEqual(flu_vaccine.date_applied, datetime.date(2017, 12, 30))
        self.assertEqual(flu_vaccine.admission_note, self.admission_note)

    def test_valid_data_vaccine_not_applied(self):
        form = FluVaccineForm({
            'was_applied': False,
        })
        self.assertTrue(form.is_valid())
        flu_vaccine = form.save_fk(self.admission_note)
        self.assertEqual(flu_vaccine.was_applied, False)
        self.assertEqual(flu_vaccine.date_applied, None)
        self.assertEqual(flu_vaccine.admission_note, self.admission_note)

    def test_valid_blank_data_vaccine_not_applied(self):
        form = FluVaccineForm({})
        self.assertTrue(form.fields['date_applied'], None)
        self.assertTrue(form.fields['was_applied'], None)
        self.assertTrue(form.is_valid(), True)

    def test_invalid_data_vaccine_applied_no_date_provided(self):
        form = FluVaccineForm({
            'was_applied': False,
            'date_applied': "09/12/2017",
            'admission_note': self.admission_note,
        })
        self.assertTrue(form.is_valid(), False)


class AdmissionNoteFormTest(TestCase):

    def test_blank_invalid_data(self):
        form = AdmissionNoteForm({})
        self.assertFalse(form.is_valid())

    def test_valid_data(self):
        form = AdmissionNoteForm({
            'id_gal_origin': "123",
        })
        self.assertTrue(form.is_valid())

    def test_save_object(self):
        form = AdmissionNoteForm({
            'id_gal_origin': "123",
        })
        admission_note = form.save()
        self.assertEqual(admission_note.id_gal_origin, "123")


class PatientFormTest(TestCase):

    def test_blank_invalid_data(self):
        form = PatientForm({})
        self.assertFalse(form.is_valid())

    def test_valid_data(self):
        form = PatientForm({
            'name': "Gabriel Test Name",
        })
        self.assertTrue(form.is_valid())

    def test_save_object(self):
        form = PatientForm({
            'name': "Gabriel Test Name",
        })
        patient = form.save()
        self.assertEqual(patient.name, "Gabriel Test Name")
        self.assertEqual(
            patient.name, Patient.objects.filter(
                name=patient.name).first().name)

