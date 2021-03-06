import unittest

import pytest

from labsys.app import create_app, db
from labsys.admissions.service import upsert_symptom
from labsys.admissions.models import Symptom, ObservedSymptom, Admission

from . import mock


# @pytest.mark.skip
class TestAdmissionServices(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.symp_01 = Symptom(name='symptom1')
        db.session.add(self.symp_01)

        self.symp_02 = Symptom(name='symptom2')
        db.session.add(self.symp_02)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_upsert_symptom_to_admission(self):
        # TODO: test excluding
        admission = mock.admission()
        db.session.add(admission)
        db.session.commit()
        obs_symptom_dict_01 = {
            'symptom_id': self.symp_01.id,
            'observed': True,
            'details': 'I do care',
        }
        obs_symptom_dict_02 = {
            'symptom_id': self.symp_02.id,
            'observed': False,
            'details': 'Do not care'
        }
        # ObsSymptom01 must be created
        # Assert there is no symptom observed in the admission
        self.assertEqual(len(admission.symptoms), 0)
        upsert_symptom(admission.id, obs_symptom_dict_01)
        # Assert there is ONE symptom observed in the admission
        self.assertEqual(len(admission.symptoms), 1)
        # Assert it's pointing to the right symptom and admission
        obs_symptom_01 = admission.symptoms[0]
        self.assertEqual(obs_symptom_01.symptom_id, self.symp_01.id)
        self.assertEqual(obs_symptom_01.admission_id, admission.id)
        # And assert it has the correct values
        self.assertEqual(obs_symptom_01.observed, True)
        self.assertEqual(obs_symptom_01.details, 'I do care')
        self.assertEqual(obs_symptom_01.symptom.name, 'symptom1')

        # ObsSymptom01 must NOT be created but UPDATED
        obs_symptom_dict_01['observed'] = False
        upsert_symptom(admission.id, obs_symptom_dict_01)
        # Assert there is ONE symptom observed in the admission
        self.assertEqual(len(admission.symptoms), 1)
        self.assertEqual(len(ObservedSymptom.query.all()), 1)
        # Assert it's value has been updated
        self.assertEqual(admission.symptoms[0].observed, False)

        # ObsSymptom02 must be created and everything else remains the same
        upsert_symptom(admission.id, obs_symptom_dict_02)
        self.assertEqual(len(admission.symptoms), 2)
        obs_symptom_02 = admission.symptoms[1]
        self.assertEqual(obs_symptom_02.observed, False)
        self.assertEqual(obs_symptom_02.details, 'Do not care')
        self.assertEqual(obs_symptom_02.symptom.name, 'symptom2')
