#!/usr/bin/env python
import os
from app import create_app, db

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

import app.models as models
from app.models import (
    User, Role, Admission, Symptom, ObservedSymptom, Vaccine, Method, Sample,
    Patient, CdcExam, Hospitalization, UTIHospitalization, ClinicalEvolution,
    Country, Region, State, City, Address,
)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
admin = Admin(app, name='labsys', template_mode='bootstrap3')
mail = Mail(app)

# region Add ModelView
admin.add_views(
    ModelView(User, db.session),
    ModelView(Role, db.session),
    ModelView(Admission, db.session),
    ModelView(Patient, db.session),
    ModelView(Address, db.session),
    ModelView(Sample, db.session),
    ModelView(CdcExam, db.session),
    ModelView(Vaccine, db.session),
    ModelView(Hospitalization, db.session),
    ModelView(UTIHospitalization, db.session),
    ModelView(ClinicalEvolution, db.session),
    ModelView(ObservedSymptom, db.session),
    ModelView(Method, db.session),
    ModelView(Symptom, db.session),
    ModelView(Country, db.session),
    ModelView(Region, db.session),
    ModelView(State, db.session),
    ModelView(City, db.session),
)
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
    # from app.models import ...

    upgrade()

    # each model responsible for inserting itself?



if __name__ == '__main__':
    manager.run()
