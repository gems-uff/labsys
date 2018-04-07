import unittest

from labsys.app import create_app, db
from labsys.admissions.models import (
    Patient, Address, Admission, Symptom, ObservedSymptom, Method, Sample,
    CdcExam, Vaccine, Hospitalization, UTIHospitalization, ClinicalEvolution,)
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

    def test_admission_dated_event_1to1_relationship(self):
        '''
        Where dated event is a vaccine, hospitalizaion, utihospitalization or
        clinicalEvolution.
        That's why their constructor must be the same as MockDatedEvent.
        '''
        # Setup
        admission = mock.admission()
        vaccine = mock.dated_event(Vaccine)
        # Add to admission
        admission.vaccine = vaccine
        # Assert they are linked
        self.assertEqual(vaccine.admission.vaccine, vaccine)
        # Overrides previous vaccine (since it's one-to-one)
        vaccine2 = mock.dated_event(Vaccine)
        vaccine2.admission = admission
        # Assert it was replaced
        self.assertNotEqual(admission.vaccine, vaccine)
        self.assertEqual(admission.vaccine, vaccine2)
        # Ensures commit works
        db.session.add(admission)
        db.session.commit()
        self.assertEqual(vaccine2.id, 1)
        self.assertIsNone(vaccine.id)
        self.assertEqual(len(Admission.query.all()), 1)
        self.assertEqual(len(Vaccine.query.all()), 1)
        # Ensures cascade all, delete-orphan works
        db.session.delete(admission)
        db.session.commit()
        self.assertEqual(len(Admission.query.all()), 0)
        self.assertEqual(len(Vaccine.query.all()), 0)

    def test_admission_symptoms_1toM_relationship(self):
        # Generate mock models
        admission = mock.admission()
        obs_symptom0 = ObservedSymptom(
            observed=True,
            details='obs symptom details',
            admission=admission,
            symptom=Symptom(name='symptom1', primary=True),
        )
        obs_symptom1 = ObservedSymptom(
            observed=False,
            details='obs symptom details',
            admission=admission,
            symptom=Symptom(name='symptom2', primary=True),
        )
        # Assert relationship between is setup
        self.assertEqual(len(admission.symptoms), 2)
        self.assertEqual(obs_symptom0.admission, obs_symptom1.admission)
        self.assertEqual(admission.symptoms[0], obs_symptom0)
        self.assertEqual(admission.symptoms[1], obs_symptom1)
        # Assert they are correctly commited
        db.session.add(admission)
        db.session.commit()
        # Assert symptoms have the same admission_id
        self.assertEqual(obs_symptom0.admission_id, obs_symptom1.admission_id)
        # Assert cascade all, delete-orphan works
        db.session.delete(admission)
        db.session.commit()
        self.assertEqual(len(Admission.query.all()), 0)
        self.assertEqual(len(ObservedSymptom.query.all()), 0)
