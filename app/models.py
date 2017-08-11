import operator
from functools import reduce

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import asc, desc, orm, UniqueConstraint
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import asc

from flask import current_app

from . import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    VIEW = 0x01
    CREATE = 0x02
    EDIT = 0x04
    DELETE = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.VIEW, True),
            'Staff': (Permission.VIEW | Permission.EDIT | Permission.CREATE,
                      False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    stock_mail_alert = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    transactions = db.relationship(
        'Transaction', backref='user', lazy='dynamic')

    @classmethod
    def get_stock_alert_emails(cls):
        return [
            u.email for u in User.query.all()
            if u.is_administrator() and u.stock_mail_alert
        ]

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['LABSYS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def generate_confirmation_token(self, expiration_seconds=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        return serializer.dumps({'confirm': self.id})

    def confirm(self, token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


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


class Product(db.Model):
    # TODO: change parent_id to child_it in order to not allow a product to have
    # more than one type of subproduct
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    manufacturer = db.Column(db.String(128))
    catalog = db.Column(db.String(128))
    stock_unit = db.Column(db.Integer, default=1)
    min_stock = db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    subproduct = db.relationship(
        'Product', backref='parent', uselist=False, remote_side=[id])
    transactions = db.relationship(
        'Transaction', backref='product', lazy='dynamic')
    stock_products = db.relationship(
        'StockProduct', backref='product', lazy='dynamic')

    @property
    def is_unitary(self):
        return self.stock_unit == 1

    @classmethod
    def get_products(cls, unitary_only=False):
        products = cls.query.order_by(asc(cls.name)).all()
        if unitary_only:
            return [p for p in products if p.is_unitary]
        return products

    @classmethod
    def get_products_by_manufacturer(cls, manufacturer, unitary_only=False):
        products = cls.query.order_by(asc(cls.id)).filter_by(
            manufacturer=manufacturer).all()
        if unitary_only:
            return [p for p in products if p.is_unitary]
        return products

    @classmethod
    def get_product_by_catalog(cls, catalog, unitary_only=False):
        products = cls.query.order_by(asc(cls.id)).filter_by(
            catalog=catalog).first()
        if unitary_only:
            return [p for p in products if p.is_unitary]
        return products

    def __repr__(self):
        return '<Product[{}], cat: {}>'.format(self.id, self.name)

    def __str__(self):
        return '<Product[{}], cat: {}>'.format(self.id, self.name)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    invoice_type = db.Column(db.String(64))
    invoice = db.Column(db.String(64))
    financier = db.Column(db.String(128))
    details = db.Column(db.String(256))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    stock_product_id = db.Column(db.Integer,
                                 db.ForeignKey('stock_products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def get_product_amount(cls, product):
        id = product[0]
        allotment = product[1]
        return cls.query.filter_by(product_id=id, allotment=allotment).count()

    @classmethod
    def get_transactions_ordered(cls):
        return cls.query.order_by(desc(cls.transaction_date)).all()

    def __repr__(self):
        return '{} : {}'.format(self.transaction_date, self.product.name[:10])


class StockProduct(db.Model):
    __tablename__ = 'stock_products'
    __table_args__ = (UniqueConstraint(
        'product_id', 'allotment', name='stock_product'), )
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    allotment = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    transactions = db.relationship(
        'Transaction', backref='stock_product', lazy='dynamic')

    @classmethod
    def get_products_in_stock(cls):
        return cls.query.filter(cls.amount > 0).order_by(asc(cls.id)).all()

    @classmethod
    def count_total_stock_of_product(cls, product_id):
        catalog_product = Product.query.get(product_id)
        amounts_in_stock = [sp.amount for sp in catalog_product.stock_products]
        return reduce(operator.add, amounts_in_stock)

    def __repr__(self):
        return '<StockProduct[{}]: {}, lote {}>'.format(
            self.id, self.product.name[:10], self.allotment)


class PreAllowedUser(db.Model):
    """Table storing users that are directly added as 'Staff'"""
    __tablename__ = 'pre_allowed_users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128))

    @classmethod
    def get_emails(cls):
        return [u.email for u in cls.query.all()]
