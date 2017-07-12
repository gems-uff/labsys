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
        'Vaccine', backref='admission', uselist=False)
    symptoms = db.relationship(
        'ObservedSymptom', backref='admission', lazy='dynamic')
    samples = db.relationship(
        'Sample', backref='admission', lazy='dynamic')

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

