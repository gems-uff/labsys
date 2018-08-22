#!/usr/bin/env python
import os

from flask_admin.menu import MenuLink
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

import labsys.admissions.forms as forms
import labsys.admissions.models as models
import labsys.inventory.models as im
from labsys.admissions.models import (
    Address, Admission, Antiviral, InfluenzaExam, ClinicalEvolution, Hospitalization,
    Method, ObservedRiskFactor, ObservedSymptom, Patient, RiskFactor, Sample,
    Symptom, UTIHospitalization, Vaccine, XRay)
from labsys.app import create_app
from labsys.auth.models import PreAllowedUser, Role, User
from labsys.auth.views import ProtectedModelView
from labsys.extensions import admin, db

app = create_app(os.environ.get('FLASK_CONFIG'))
manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)

# region Add ModelView
admin.add_views(
    ProtectedModelView(User, db.session),
    ProtectedModelView(Role, db.session),
    ProtectedModelView(PreAllowedUser, db.session),
    ProtectedModelView(im.Product, db.session),
    ProtectedModelView(im.Transaction, db.session),
    ProtectedModelView(im.StockProduct, db.session),
    ProtectedModelView(im.Specification, db.session),
    ProtectedModelView(im.Order, db.session),
    ProtectedModelView(im.OrderItem, db.session),
    ProtectedModelView(Symptom, db.session),
    ProtectedModelView(ObservedSymptom, db.session),
    ProtectedModelView(Admission, db.session),
    ProtectedModelView(Sample, db.session),
    ProtectedModelView(InfluenzaExam, db.session),
    ProtectedModelView(Method, db.session),
    ProtectedModelView(RiskFactor, db.session),
    ProtectedModelView(ObservedRiskFactor, db.session),
    ProtectedModelView(Vaccine, db.session),
    ProtectedModelView(Hospitalization, db.session),
    ProtectedModelView(UTIHospitalization, db.session),
    ProtectedModelView(ClinicalEvolution, db.session),
    ProtectedModelView(Antiviral, db.session),
    ProtectedModelView(XRay, db.session),
)
admin.add_link(MenuLink(name='Voltar para Dashboard', url=('/')))

# endregion


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, f=forms, m=models)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the tests."""
    if app.config['DATABASE_URI_ENV_KEY'] != 'TEST_DATABASE_URL':
        raise EnvironmentError(
            'Trying to run tests outside testing environment!')
    import pytest
    rv = pytest.main(['--verbose'])
    exit(rv)


@manager.command
def load_initial_data():
    """Load initial models data"""
    import labsys.utils.data_loader as dl
    dl.load_data(db)


@manager.command
def deploy():
    """Run deployment tasks"""
    from flask_migrate import upgrade
    upgrade()
    Role.insert_roles()
    User.insert_admin()
    Method.insert_methods()
    im.Stock.insert_stock('Reativos')


if __name__ == '__main__':
    manager.run()
