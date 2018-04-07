from sqlalchemy.ext.declarative import declared_attr
from ..extensions import db


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
