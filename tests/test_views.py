import unittest
import datetime
from flask import current_app, url_for, get_flashed_messages
from app import create_app, db
from app.models import *


class TestCreateAdmissionView(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        self.valid_admission_form = {
            'id_lvrs_intern': '011/2012',
            'samples-0-collection_date': '12/12/2012',
            'samples-0-admission_date': '13/12/2012',
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_duplicate_id_lvrs_intern(self):
        data = self.valid_admission_form
        a = Admission(id_lvrs_intern=data['id_lvrs_intern'])
        db.session.add(a)
        db.session.commit()
        duplicate_id_lvrs_intern = 'Número Interno já cadastrado!'
        response = self.client.post(
            url_for('main.create_admission'), data=data, follow_redirects=True)
        self.assertTrue(
            duplicate_id_lvrs_intern in response.get_data(as_text=True))
        self.assertEqual(len(Admission.query.all()), 1)

    def test_create_valid_admission(self):
        data = self.valid_admission_form
        self.assertEqual(len(Admission.query.all()), 0)
        response = self.client.post(
            url_for('main.create_admission'), data=data, follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        admission = Admission.query.first()
        self.assertEqual(admission.id_lvrs_intern, data['id_lvrs_intern'])
        self.assertEqual(admission.samples.first().collection_date,
                         datetime.date(2012, 12, 12))
        self.assertEqual(admission.samples.first().admission_date,
                         datetime.date(2012, 12, 13))

    def test_admissions_listing(self):
        id_lvrs_intern = '0001/2017'
        collection_date = datetime.date(2017, 12, 22)
        a = Admission(id_lvrs_intern=id_lvrs_intern)
        s1 = Sample(collection_date=collection_date, admission=a)
        db.session.add(a)
        db.session.commit()
        response = self.client.get(url_for('main.list_admissions'))
        data = response.get_data(as_text=True)
        self.assertTrue(response.status_code == 200)
        self.assertIn('0001/2017', data)
        self.assertIn('22/12/2017', data)
