from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import asc

from ..extensions import db

from .mixins import AdmissionOneToOneMixin, DatedEvent

'''
Limitações conhecidas
- O Patient só pode ter um Address, ou seja, a pergunta "Quando ele foi admitido no ano X, ele morava onde?" não pode ser respondida.
    - Podemos futuramente pensar em uma maneira da Admission saber disso, ex.: Admission.patient_residence
- Quando uma Admission é deletada, os "eventos" também o são: Vaccine, Hospitalization, UTIHospitalization e ClinicalEvolution
'''

# TODO: Add nullable to columns which are not present in initial importing CSV
# TODO: Abstract ObservedSymptoms/Symptoms and ObservedRiskFactors, RiskFactors


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
    # maybe it should be in a separate table
    secondary_symptoms = db.Column(db.String(512), nullable=True)
    secondary_risk_factors = db.Column(db.String(512), nullable=True)
    # relationships
    samples = db.relationship(
        'Sample', backref='admission', lazy='dynamic')

    def __repr__(self):
        return '<Admission[{}]: {}>'.format(self.id, self.id_lvrs_intern)


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ObservedSymptom(db.Model):
    __tablename__ = 'observed_symptoms'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    observed = db.Column(db.Boolean)
    details = db.Column(db.String(255))
    # Relationships
    admission = db.relationship('Admission', backref=db.backref(
        'symptoms', cascade='all, delete-orphan'))
    symptom = db.relationship('Symptom', backref=db.backref(
        'observations', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<ObservedSymptom[{}]: {}>'.format(self.id, self.symptom.name)


class RiskFactor(db.Model):
    __tablename__ = 'risk_factors'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ObservedRiskFactor(db.Model):
    __tablename__ = 'observed_risk_factors'

    id = db.Column(db.Integer, primary_key=True)
    # FK
    risk_factor_id = db.Column(db.Integer, db.ForeignKey('risk_factors.id'))
    admission_id = db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    observed = db.Column(db.Boolean)
    details = db.Column(db.String(255))
    # Relationships
    admission = db.relationship('Admission', backref=db.backref(
        'risk_factors', cascade='all, delete-orphan'))
    risk_factor = db.relationship('RiskFactor', backref=db.backref(
        'observations', cascade='all, delete-orphan'))

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


# TODO: merge Antiviral and XRay
class Antiviral(AdmissionOneToOneMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    @declared_attr
    def admission_id(cls):
        return db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    usage = db.Column(db.String(255), nullable=True)
    other = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)


class XRay(AdmissionOneToOneMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    @declared_attr
    def admission_id(cls):
        return db.Column(db.Integer, db.ForeignKey('admissions.id'))
    # Attributes
    usage = db.Column(db.String(255), nullable=True)
    other = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
