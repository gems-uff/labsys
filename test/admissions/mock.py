from labsys.admissions.models import (
    Patient, Address, Admission, Vaccine, AdmissionOneToOneMixin, DatedEvent,
    ObservedSymptom, Symptom,
)


def generate_mock(MockClass, **kwargs):
    mock_class = MockClass(**kwargs)
    return mock_class


def patient():
    return Patient(
        name='Pat Name',
        birth_date='2018-01-01',
        age=10,
        age_unit='A',
        gender='H',
    )


def address():
    return Address(
        country='Brasil',
        state='RJ',
        city='Niterói',
        neighborhood='Icaraí',
    )


def admission():
    return Admission(
        id_lvrs_intern='lvrs0001',
        state='RJ',
        city='Niterói',
        first_symptoms_date='2018-01-01',
        semepi_symptom=12,
        health_unit='Unidade de saude 1',
        requesting_institution='Solicitante 1',
        details='detalhes admission',
    )


def dated_event(_class, **kwargs):
    return _class(**kwargs)
