from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import asc
from ..extensions import db


class TimeStampedModelMixin(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


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


class PrimarySecondaryEntity(db.Model):
    '''
    A named entity that is classified as primary or secondary
    '''
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String(64))
    primary = db.Column(db.Boolean)

    @classmethod
    def get_primary(cls):
        return cls.query.filter(
            cls.primary is True).order_by(asc(cls.name)).all()

    @classmethod
    def get_secondary(cls):
        return cls.query.filter(
            cls.primary is False).order_by(asc(cls.name)).all()

    def __repr__(self):
        return '<{}[{}]: {}, Primary: {}>'.format(
            self.__class__.__name__, self.id, self.name, self.primary)
