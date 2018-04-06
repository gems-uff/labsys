import unittest

from labsys.app import create_app, db
from labsys.admissions.models import (
    Patient, Address, Admission, Vaccine, Hospitalization, UTIHospitalization,
    ClinicalEvolution, Symptom, ObservedSymptom, Method, Sample, CdcExam)

from . import mock


class TestAuthenticationViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_patient_address_1to1_relationship(self):
        patient = mock.patient()
        residence = mock.address()
        patient.residence = residence
        self.assertEqual(patient.residence.patient, patient)
        db.session.add(patient)
        db.session.commit()

    def test_patient_admission_1toM_relationship(self):
        patient = mock.patient()
        admission = mock.admission()
        patient.admissions.append(admission)
        self.assertEqual(admission.patient, patient)
        self.assertEqual(len(patient.admissions.all()), 1)
        patient = mock.patient()
        admission = mock.admission()
        admission.patient = patient
        self.assertEqual(admission.patient, patient)
        self.assertEqual(len(patient.admissions.all()), 1)

    def test_admission_event_1to1_relationship(self):
        '''
        where event is a vaccine, hospitalizaion, utihospitalization or
        clinicalEvolution
        '''
        # add vaccine to admission
        admission = mock.admission()
        vaccine = mock.vaccine()
        admission.vaccine = vaccine
        self.assertEqual(vaccine.admission.vaccine, vaccine)
        # overrides previous vaccine (since it's one-to-one)
        vaccine2 = mock.vaccine()
        vaccine2.admission = admission
        self.assertNotEqual(admission.vaccine, vaccine)
        self.assertEqual(admission.vaccine, vaccine2)
        # ensures commit works
        db.session.add(admission)
        db.session.commit()
        self.assertEqual(vaccine2.id, 1)
        # ensures cascade all, delete-orphan works
        db.session.delete(admission)
        db.session.commit()
        query_admission = admission.query.all()
        query_vaccine = vaccine.query.all()
        self.assertEqual(len(query_admission), 0)
        self.assertEqual(len(query_vaccine), 0)
