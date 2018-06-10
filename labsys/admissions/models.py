from sqlalchemy import asc
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db
from .mixins import AdmissionOneToOneMixin, DatedEvent, TimeStampedModelMixin


class Patient(TimeStampedModelMixin, db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    age_unit = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    # Relationships
    residence = db.relationship('Address', backref='patient', uselist=False)
    admissions = db.relationship(
        'Admission', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient[{}]: {}>'.format(self.id, self.name)

    csv_dict = {
        'name': 'Nome Profissional de Saúde',
        'birth_date': 'Data de Nascimento',
        'age': 'Idade',
        'age_unit': 'Tipo Idade',
        'gender': 'Sexo',
    }

    @classmethod
    def model_from_csv(cls, csv_row):
        p = Patient()
        p.name = csv_row.get(cls.csv_dict['name'])
        p.birth_date = datetime.datetime.strptime(
            csv_row.get(cls.csv_dict['birth_date']), '%d/%m/%Y')
        p.age = int(csv_row.get(cls.csv_dict['age']))
        p.age_unit = csv_row.get(cls.csv_dict['age_unit'])
        p.gender = csv_row.get(cls.csv_dict['gender'])
        return p


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
    zone = db.Column(db.String(255))
    details = db.Column(db.String(255))

    def __repr__(self):
        return '<Address[{}]: Pat{}>'.format(self.id, self.patient)

    csv_dict = {
        'country': 'País de Residência',
        'state': 'Estado de Residência',
        'city': 'Município de Residência',
        'neighborhood': 'Bairro',
        'zone': 'Zona',
        # 'details': '', => does not exist in csv
    }

    @classmethod
    def model_from_csv(cls, csv_row):
        a = Address()
        a.country = csv_row.get(cls.csv_dict['country'])
        a.state = csv_row.get(cls.csv_dict['state'])
        a.city = csv_row.get(cls.csv_dict['city'])
        a.neighborhood = csv_row.get(cls.csv_dict['neighborhood'])
        a.zone = csv_row.get(cls.csv_dict['zone'])
        return a


class Admission(TimeStampedModelMixin, db.Model):
    __tablename__ = 'admissions'
    id = db.Column(db.Integer, primary_key=True)
    # FK
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    # Attributes
    id_lvrs_intern = db.Column(db.String(255), unique=True, nullable=False)
    state = db.Column(db.String(255))
    city = db.Column(db.String(255))
    first_symptoms_date = db.Column(db.Date)
    semepi_symptom = db.Column(db.Integer)
    health_unit = db.Column(db.String(255))
    requesting_institution = db.Column(db.String(128))
    details = db.Column(db.String(255))
    # maybe it should be in a separate table
    secondary_symptoms = db.Column(db.String(512), nullable=True)
    secondary_risk_factors = db.Column(db.String(512), nullable=True)
    # relationships
    samples = db.relationship('Sample', backref='admission', lazy='dynamic')

    def __repr__(self):
        return '<Admission[{}]: {}>'.format(self.id, self.id_lvrs_intern)

    csv_dict = {
        'id_lvrs_intern': 'Número Interno',
        'state': 'Estado de Residência',
        'city': 'Município de Residência',
        'first_symptoms_date': 'Data do 1º Sintomas',
        # 'semepi_symptom': '', => does not exist in csv, might be computed
        'health_unit': 'Laboratório de Cadastro',
        'requesting_institution': 'Unidade Solicitante',
        # 'details': '', => does not exist in csv
    }

    @classmethod
    def model_from_csv(cls, csv_row):
        a = Admission()
        a.id_lvrs_intern = csv_row.get(cls.csv_dict['id_lvrs_intern'],
                                       'NOT FOUND')
        a.state = csv_row.get(cls.csv_dict['state'], 'NOT FOUND')
        return a


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
    admission = db.relationship(
        'Admission',
        backref=db.backref('symptoms', cascade='all, delete-orphan'))
    symptom = db.relationship(
        'Symptom',
        backref=db.backref('observations', cascade='all, delete-orphan'))

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
    admission = db.relationship(
        'Admission',
        backref=db.backref('risk_factors', cascade='all, delete-orphan'))
    risk_factor = db.relationship(
        'RiskFactor',
        backref=db.backref('observations', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<ObservedRiskFactor[{}]: {}>'.format(self.id,
                                                     self.risk_factor.name)


class Method(db.Model):
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(64))

    @staticmethod
    def insert_methods():
        method_name = 'Outro'
        other_method = Method.query.filter_by(name=method_name).first()
        if other_method is None:
            other_method = Method(name=method_name)
        db.session.add(other_method)
        db.session.commit()

    def __repr__(self):
        return '<Method[{}]: {}>'.format(self.id, self.name)


class Sample(TimeStampedModelMixin, db.Model):

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

    def __repr__(self):
        return '<Sample[{}]: {}>'.format(self.id, self.collection_date)


class CdcExam(TimeStampedModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # FKs
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    # Attributes
    flu_type = db.Column(db.String(16))
    flu_subtype = db.Column(db.String(16))
    dominant_ct = db.Column(db.Numeric(12, 2), nullable=True)
    details = db.Column(db.String(255), nullable=True)
    # Relationship
    sample = db.relationship(
        'Sample',
        backref=db.backref(
            'cdc_exam', cascade='all, delete-orphan', uselist=False))

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
