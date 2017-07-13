from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    admissions = db.relationship(
        'Admission', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient[{}]: {}>'.format(self.id, self.name)


class Admission(db.Model):
    __tablename__ = 'admissions'
    id = db.Column(db.Integer, primary_key=True)
    id_lvrs_intern = db.Column(db.String(32), unique=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    vaccine = db.relationship(
        'Vaccine', backref='admission', uselist=False,
        cascade='all, delete-orphan')
    hospitalization = db.relationship(
        'Hospitalization', backref='admission', uselist=False,
        cascade='all, delete-orphan')
    uti_hospitalization = db.relationship(
        'UTIHospitalization', backref='admission', uselist=False,
        cascade='all, delete-orphan')
    clinical_evolution = db.relationship(
        'ClinicalEvolution', backref='admission', uselist=False,
        cascade='all, delete-orphan')
    symptoms = db.relationship(
        'ObservedSymptom', backref='admission', lazy='dynamic')
    samples = db.relationship('Sample', backref='admission', lazy='dynamic')

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
        return cls.query.filter(cls.primary==True).all()

    @classmethod
    def get_secondary_symptoms(cls):
        return cls.query.filter(cls.primary==False).all()

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
    collection_date = db.Column(db.Date())
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    cdc_exams = db.relationship('CdcExam', backref='sample', lazy='dynamic')

    def __repr__(self):
        return '<Sample[{}]: {}>'.format(self.id, self.collection_date)


class CdcExam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(255))
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))

    def __repr__(self):
        return '<CdcExam[{}]: {}>'.format(self.id, self.details)


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name_en_us = db.Column(db.String(255))
    name_pt_br = db.Column(db.String(255))
    abbreviation = db.Column(db.String(2))
    bacen_code = db.Column(db.Integer)
    regions = db.relationship('Region', backref='region', lazy='dynamic')


    def __repr__(self):
        return '<Country[{}/{}]>'.format(self.name_en_us, self.initials)

    def __str__(self):
        return '{}/{}'.format(self.name_pt_br, self.initials)


class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    name = db.Column(db.String(16))
    region_code = db.Column(db.Integer)
    states = db.relationship('State', backref='region', lazy='dynamic')


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    name = db.Column(db.String(64))
    uf_code = db.column(db.String(2))
    ibge_code = db.Column(db.Integer)
    cities = db.relationship('City', backref='city', lazy='dynamic')


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    ibge_code = db.Column(db.Integer)
    name = db.Column(db.String(128))


class Residence(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    # TODO: normalize?
    country = db.Column(db.String(255))
    uf_code = db.Column(db.String(2))
    city = db.Column(db.String(128))
    neighborhood = db.Column(db.String(255))



