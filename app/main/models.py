import operator
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import asc, desc, orm, UniqueConstraint, func

from flask import current_app

from app import db, login_manager


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    age_unit = db.Column(db.String(1))
    gender = db.Column(db.String(1))
    residence = db.relationship('Address', backref='patient', uselist=False)
    admissions = db.relationship(
        'Admission', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient[{}]: {}>'.format(self.id, self.name)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    neighborhood = db.Column(db.String(255))
    zone = db.Column(db.Integer)
    details = db.Column(db.String(255))

    def __repr__(self):
        return '<Address[{}]: Pat{}>'.format(self.id, self.patient_id)


class Admission(db.Model):
    __tablename__ = 'admissions'
    id = db.Column(db.Integer, primary_key=True)
    id_lvrs_intern = db.Column(db.String(32), unique=True)
    first_symptoms_date = db.Column(db.Date)
    semepi_symptom = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    health_unit = db.Column(db.String(128))
    requesting_institution = db.Column(db.String(128))
    details = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
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
    samples = db.relationship('Sample', backref='_admission', lazy='dynamic')

    def __repr__(self):
        return '<Admission[{}]: {}>'.format(self.id, self.id_lvrs_intern)


class Vaccine(db.Model):
    __tablename__ = 'vaccines'
    id = db.Column(db.Integer, primary_key=True)
    applied = db.Column(db.Boolean, nullable=True)
    last_dose_date = db.Column(db.Date())
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))

    def __repr__(self):
        return '<Vaccine[{}]: {}>'.format(self.id, self.applied)


class Hospitalization(db.Model):
    __tablename__ = 'hospitalizations'
    id = db.Column(db.Integer, primary_key=True)
    occurred = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.Date())
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))

    def __repr__(self):
        return '<Hospitalization[{}]: {}>'.format(self.id, self.occurred)


class UTIHospitalization(db.Model):
    __tablename__ = 'uti_hospitalizations'
    id = db.Column(db.Integer, primary_key=True)
    occurred = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.Date())
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))

    def __repr__(self):
        return '<UTI Hospitalization[{}]: {}>'.format(self.id, self.occurred)


class ClinicalEvolution(db.Model):
    __tablename__ = 'clinical_evolutions'
    id = db.Column(db.Integer, primary_key=True)
    death = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.Date())
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))

    def __repr__(self):
        return '<ClinicalEvolution[{}]: {}>'.format(self.id, self.death)


class Symptom(db.Model):
    __tablename__ = 'symptoms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    primary = db.Column(db.Boolean)
    observed_symptoms = db.relationship(
        'ObservedSymptom', backref='symptom', lazy='dynamic')

    @classmethod
    def get_primary_symptoms(cls):
        return cls.query.filter(
            cls.primary == True).order_by(asc(Symptom.id)).all()

    @classmethod
    def get_secondary_symptoms(cls):
        return cls.query.filter(
            cls.primary == False).order_by(asc(Symptom.id)).all()

    def __repr__(self):
        return '<Symptom[{}]: {}>'.format(self.id, self.name)


class ObservedSymptom(db.Model):
    __tablename__ = 'observed_symptoms'
    id = db.Column(db.Integer, primary_key=True)
    observed = db.Column(db.Boolean)
    details = db.Column(db.String(255))
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))

    def __repr__(self):
        return '<ObservedSymptom[{}]: {}>'.format(self.id, self.symptom.name)


class Method(db.Model):
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    primary = db.Column(db.Boolean)
    samples = db.relationship('Sample', backref='method', lazy='dynamic')

    def __repr__(self):
        return '<Method[{}]: {}>'.format(self.id, self.name)


class Sample(db.Model):

    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    admission_date = db.Column(db.Date())
    collection_date = db.Column(db.Date())
    semepi = db.Column(db.Integer)
    details = db.Column(db.String(128))
    _ordering = db.Column(db.Integer)
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
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
    flu_type = db.Column(db.String(16))
    flu_subtype = db.Column(db.String(16))
    dominant_ct = db.Column(db.Integer)
    details = db.Column(db.String(255))
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))

    def __repr__(self):
        return '<CdcExam[{}]: {}>'.format(self.id, self.details)


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name_pt_br = db.Column(db.String(255))
    abbreviation = db.Column(db.String(2))
    name_en_us = db.Column(db.String(255))
    bacen_code = db.Column(db.Integer)
    regions = db.relationship('Region', backref='country', lazy='dynamic')
    addresses = db.relationship('Address', backref='country', lazy='dynamic')

    def __repr__(self):
        return '<Country[{}/{}]>'.format(self.name_en_us, self.abbreviation)

    def __str__(self):
        return '{}/{}'.format(self.name_pt_br, self.abbreviation)


class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    name = db.Column(db.String(16))
    region_code = db.Column(db.Integer)
    states = db.relationship('State', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<Region[{}: {}]>'.format(self.name, self.region_code)

    def __str__(self):
        return '{}'.format(self.name)


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    name = db.Column(db.String(64))
    uf_code = db.Column(db.String(2))
    ibge_code = db.Column(db.Integer)
    cities = db.relationship('City', backref='state', lazy='dynamic')
    addresses = db.relationship('Address', backref='state', lazy='dynamic')
    admissions = db.relationship('Admission', backref='state', lazy='dynamic')

    def __repr__(self):
        return '<State[{}/{}]>'.format(self.name, self.uf_code)

    def __str__(self):
        return '{}/{}'.format(self.name, self.uf_code)


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    ibge_code = db.Column(db.Integer)
    name = db.Column(db.String(128))
    addresses = db.relationship('Address', backref='city', lazy='dynamic')
    admissions = db.relationship('Admission', backref='city', lazy='dynamic')

    def __repr__(self):
        return '<City[{}/{}]>'.format(self.name, self.state.uf_code
                                      if self.state is not None else 'None')

    def __str__(self):
        return '{}/{}'.format(self.name, self.state.uf_code
                              if self.state is not None else 'None')
