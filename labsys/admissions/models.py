from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import asc

from ..extensions import db

'''
- O Patient só pode ter um Address, ou seja, a pergunta "Quando ele foi admitido no ano X, ele morava onde?" não pode ser respondida.
    - Podemos futuramente pensar em uma maneira da Admission saber disso, ex.: Admission.patient_residence
- Quando uma Admission é deletada, os "eventos" também o são: Vaccine, Hospitalization, UTIHospitalization e ClinicalEvolution
'''

# TODO: Remove cities, states, regions, countries
# TODO: Add RiskFactor to Admission
# TODO: Add nullable to columns which are not present in initial importing CSV
# TODO: Abstract events (Vaccine, etc.)


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    age_unit = db.Column(db.String(1))
    gender = db.Column(db.String(1))
    # Relationships
    residence = db.relationship('Address', backref='patient', uselist=False)
    admissions = db.relationship(
        'Admission', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient[{}]: {}>'.format(self.id, self.name)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    # Attributes
    country = db.Column(db.String(255))
    state = db.Column(db.String(255))
    city = db.Column(db.String(255))
    neighborhood = db.Column(db.String(255))
    zone = db.Column(db.Integer)
    details = db.Column(db.String(255))

    def __repr__(self):
        return '<Address[{}]: Pat{}>'.format(self.id, self.patient)


class Admission(db.Model):
    __tablename__ = 'admissions'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    # Attributes
    id_lvrs_intern = db.Column(db.String(32), unique=True)
    state = db.Column(db.String(255))
    city = db.Column(db.String(255))
    first_symptoms_date = db.Column(db.Date)
    semepi_symptom = db.Column(db.Integer)
    health_unit = db.Column(db.String(128))
    requesting_institution = db.Column(db.String(128))
    details = db.Column(db.String(255))
    # Relationships
    vaccine = db.relationship(
        'Vaccine',
        backref='admission',
        uselist=False,
        cascade='all, delete-orphan')
    hospitalization = db.relationship(
        'Hospitalization',
        backref='admission',
        uselist=False,
        cascade='all, delete-orphan')
    uti_hospitalization = db.relationship(
        'UTIHospitalization',
        backref='admission',
        uselist=False,
        cascade='all, delete-orphan')
    clinical_evolution = db.relationship(
        'ClinicalEvolution',
        backref='admission',
        uselist=False,
        cascade='all, delete-orphan')
    symptoms = db.relationship(
        'ObservedSymptom', backref='admission', lazy='dynamic')
    # TODO: add risk_factors
    samples = db.relationship(
        'Sample', backref='admission', lazy='dynamic')

    def __repr__(self):
        return '<Admission[{}]: {}>'.format(self.id, self.id_lvrs_intern)


class Vaccine(db.Model):
    __tablename__ = 'vaccines'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    applied = db.Column(db.Boolean, nullable=True)
    last_dose_date = db.Column(db.Date())

    def __repr__(self):
        return '<Vaccine[{}]: {}>'.format(self.id, self.applied)


class Hospitalization(db.Model):
    __tablename__ = 'hospitalizations'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    occurred = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.Date())

    def __repr__(self):
        return '<Hospitalization[{}]: {}>'.format(self.id, self.occurred)


class UTIHospitalization(db.Model):
    __tablename__ = 'uti_hospitalizations'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    occurred = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.Date())

    def __repr__(self):
        return '<UTI Hospitalization[{}]: {}>'.format(self.id, self.occurred)


class ClinicalEvolution(db.Model):
    __tablename__ = 'clinical_evolutions'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    death = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.Date())

    def __repr__(self):
        return '<ClinicalEvolution[{}]: {}>'.format(self.id, self.death)


class Symptom(db.Model):
    __tablename__ = 'symptoms'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(64))
    primary = db.Column(db.Boolean)
    # Relationships
    observed_symptoms = db.relationship(
        'ObservedSymptom', backref='symptom', lazy='dynamic')

    @classmethod
    def get_primary_symptoms(cls):
        return cls.query.filter(
            cls.primary is True).order_by(asc(Symptom.id)).all()

    @classmethod
    def get_secondary_symptoms(cls):
        return cls.query.filter(
            cls.primary is False).order_by(asc(Symptom.id)).all()

    def __repr__(self):
        return '<Symptom[{}]: {}>'.format(self.id, self.name)


class ObservedSymptom(db.Model):
    __tablename__ = 'observed_symptoms'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    observed = db.Column(db.Boolean)
    details = db.Column(db.String(255))

    def __repr__(self):
        return '<ObservedSymptom[{}]: {}>'.format(self.id, self.symptom.name)


class Method(db.Model):
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(64))
    primary = db.Column(db.Boolean)
    # Relationships
    samples = db.relationship(
        'Sample', backref='method', uselist=False)

    def __repr__(self):
        return '<Method[{}]: {}>'.format(self.id, self.name)


class Sample(db.Model):

    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    _ordering = db.Column(db.Integer)
    admission_date = db.Column(db.Date())
    collection_date = db.Column(db.Date())
    semepi = db.Column(db.Integer)
    details = db.Column(db.String(128))
    # FKs
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Relationships
    cdc_exam = db.relationship('CdcExam', backref='sample', uselist=False)

    @hybrid_property
    def admission(self):
        return self._admission

    @admission.setter
    def admission(self, admission):
        self._admission = admission
        if self._admission is not None:
            self.ordering = len(self._admission.samples.all())
        else:
            self.ordering = -1

    @hybrid_property
    def ordering(self):
        return self._ordering

    @ordering.setter
    def ordering(self, ordering):
        self._ordering = ordering

    def __repr__(self):
        return '<Sample[{}]: {}>'.format(self.id, self.collection_date)


class CdcExam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    flu_type = db.Column(db.String(16))
    flu_subtype = db.Column(db.String(16))
    dominant_ct = db.Column(db.Integer)
    details = db.Column(db.String(255))
    # FKs
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))

    def __repr__(self):
        return '<CdcExam[{}]: {}>'.format(self.id, self.details)
