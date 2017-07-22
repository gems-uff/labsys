import unittest
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
            'id_lvrs_intern': 1,
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_duplicate_id_lvrs_intern(self):
        a = Admission(id_lvrs_intern=1)
        db.session.add(a)
        db.session.commit()
        data = {
            'id_lvrs_intern': '1',
            'samples-0-collection_date': '12/12/2012',
            'samples-0-admission_date': '13/12/2012',
        }
        duplicate_id_lvrs_intern = 'Número Interno já cadastrado!'
        response = self.client.post(
            url_for('main.create_admission'), data=data, follow_redirects=True)
        self.assertTrue(
            duplicate_id_lvrs_intern in response.get_data(as_text=True))
        self.assertTrue(
            len(Admission.query.filter_by(id_lvrs_intern='1').all()), 1)
