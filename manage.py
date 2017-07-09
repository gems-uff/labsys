#!/usr/bin/env python
import os
from app import create_app, db
from app.models import (
    User, Role, Admission, Symptom, ObservedSymptom, Vaccine, Method, Sample,
    Patient,
)
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
admin = Admin(app, name='labsys', template_mode='bootstrap3')

# region Add ModelView
admin.add_views(
    ModelView(User, db.session),
    ModelView(Role, db.session),
    ModelView(Admission, db.session),
    ModelView(Patient, db.session),
    ModelView(Vaccine, db.session),
    ModelView(Symptom, db.session),
    ModelView(ObservedSymptom, db.session),
    ModelView(Method, db.session),
    ModelView(Sample, db.session),
)
# endregion

def make_shell_context():
    return dict(
        app=app,
        db=db,
    )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
