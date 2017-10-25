#!/usr/bin/env python
import os

from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from labsys.app import create_app
from labsys.extensions import db
from labsys.auth.models import User, Role, PreAllowedUser
from labsys.auth.views import ProtectedModelView
from labsys.inventory.models import Product, Transaction, StockProduct
from labsys.admissions.models import (
    Admission, Symptom, ObservedSymptom, Vaccine, Method, Sample, Patient,
    CdcExam, Hospitalization, UTIHospitalization, ClinicalEvolution, Country,
    Region, State, City, Address,
)

app = create_app(os.environ.get('FLASK_CONFIG'))
manager = Manager(app)
migrate = Migrate(app, db)
admin = Admin(app, name='labsys', template_mode='bootstrap3')

# region Add ModelView
admin.add_views(
    ProtectedModelView(User, db.session),
    ProtectedModelView(Role, db.session),
    ProtectedModelView(PreAllowedUser, db.session),
    ProtectedModelView(Admission, db.session),
    ProtectedModelView(Patient, db.session),
    ProtectedModelView(Address, db.session),
    ProtectedModelView(Sample, db.session),
    ProtectedModelView(CdcExam, db.session),
    ProtectedModelView(Vaccine, db.session),
    ProtectedModelView(Hospitalization, db.session),
    ProtectedModelView(UTIHospitalization, db.session),
    ProtectedModelView(ClinicalEvolution, db.session),
    ProtectedModelView(ObservedSymptom, db.session),
    ProtectedModelView(Method, db.session),
    ProtectedModelView(Symptom, db.session),
    ProtectedModelView(Country, db.session),
    ProtectedModelView(Region, db.session),
    ProtectedModelView(State, db.session),
    ProtectedModelView(City, db.session),
    ProtectedModelView(Product, db.session),
    ProtectedModelView(Transaction, db.session),
    ProtectedModelView(StockProduct, db.session), )
admin.add_link(MenuLink(name='Voltar para Dashboard', url=('/')))
# endregion


def make_shell_context():
    return dict(
        app=app, db=db, User=User, Role=Role,
        Product=Product, StockProduct=StockProduct,
    )


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
    load_initial_data()


if __name__ == '__main__':
    manager.run()
