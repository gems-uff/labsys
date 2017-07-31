#!/usr/bin/env python
import os
from app import create_app, db

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

import app.models as models
from app.models import (
    User, Role, Admission, Symptom, ObservedSymptom, Vaccine, Method, Sample,
    Patient, CdcExam, Hospitalization, UTIHospitalization, ClinicalEvolution,
    Country, Region, State, City, Address,
)
from app.auth.views import ProtectedModelView

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
admin = Admin(app, name='labsys', template_mode='bootstrap3')


# region Add ModelView
admin.add_views(
    ProtectedModelView(User, db.session),
    ProtectedModelView(Role, db.session),
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
)
admin.add_link(MenuLink(name='Voltar para Dashboard', url=('/')))
# endregion


def make_shell_context():
    return dict(
        app=app,
        db=db,
        m=models,
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def load_initial_data():
    """Load initial models data"""
    import app.data_loader as dl
    dl.load_data(db)


@manager.command
def deploy():
    """Run deployment tasks"""
    from flask_migrate import upgrade
    upgrade()
    load_initial_data()



if __name__ == '__main__':
    manager.run()
