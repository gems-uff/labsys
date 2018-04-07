from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
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
    symptoms = db.relationship(
        'ObservedSymptom', backref='admission', lazy='dynamic')
    samples = db.relationship(
        'Sample', backref='admission', lazy='dynamic')

    def __repr__(self):
        return '<Admission[{}]: {}>'.format(self.id, self.id_lvrs_intern)


class AdmissionOneToOneMixin(object):
    '''
    A mixin that adds a One-to-One relationship to Admission

    The relationship considers Admission as a parent and cascades
    all to the subject using it.
    '''
    # Relationship
    @declared_attr
    def admission(cls):
        return db.relationship(
            'Admission',
            backref=db.backref(cls.__name__.lower(),
                               uselist=False,
                               cascade='all, delete-orphan'))


class DatedEvent(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True)
    occurred = db.Column(db.Boolean, nullable=True)

    # Foreign Key
    @declared_attr
    def admission_id(cls):
        return db.Column(db.Integer, db.ForeignKey('admissions.id'))

    def __repr__(self):
        return '<{}[{}]: {}>'.format(self.__class__.__name__,
                                     self.id,
                                     self.occurred)


class Vaccine(AdmissionOneToOneMixin, DatedEvent):
    __tablename__ = 'vaccines'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Hospitalization(AdmissionOneToOneMixin, DatedEvent):
    __tablename__ = 'hospitalizations'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UTIHospitalization(AdmissionOneToOneMixin, DatedEvent):
    __tablename__ = 'uti_hospitalizations'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ClinicalEvolution(AdmissionOneToOneMixin, DatedEvent):
    __tablename__ = 'clinical_evolutions'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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
    def get_primary(cls):
        return cls.query.filter(
            cls.primary is True).order_by(asc(Symptom.id)).all()

    @classmethod
    def get_secondary(cls):
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
