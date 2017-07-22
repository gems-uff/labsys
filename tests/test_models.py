import unittest
from app import create_app, db
from app.models import Sample, Admission


class SampleModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_sample_ordering(self):
        admission = Admission()
        sample1 = Sample()
        sample2 = Sample()
        sample3 = Sample()

        self.assertEqual(len(admission.samples.all()), 0)
        sample1.admission = admission
        self.assertEqual(sample1.ordering, 1)
        sample2.admission = admission
        self.assertEqual(sample2.ordering, 2)
        sample2.admission = None
        self.assertEqual(sample2.ordering, -1)
        sample3.admission = admission
        self.assertEqual(sample3.ordering, 2)

