from admission_notes.models import AdmissionNote
from patients.models import Patient, Locality


def are_forms_valid(forms):
    for form in forms:
        if not form.is_valid():
            return False
    return True


def get_admission_note(dict=False, form=False):
    admission_note = {
        'id_request_gal': 'teste_gal',
        'id_lvrs_intern': '334/2017',
        'requester': 'teste requeste',
        'health_unit': 'teste health unit',
        'state': 'RJ',
        'city': 'Niteroi',
        'admission_date': '2012-12-20',
        'details': 'Teste de details'
    }

    if not dict:
        admission_note = AdmissionNote(**admission_note)
    if form:
        admission_note['admission_date'] = '20/12/2012'
    return admission_note


def get_patient(dict=False, form=False):
    patient = {
        'name': 'Nome de Teste dos Santos',
        'birth_date': '1994-12-12',
        'age': 12,
        'age_unit': 'A',
        'gender': 'M',
        'pregnant': 6,
    }

    if not dict:
        patient = Patient(**patient)
    if form:
        patient['birth_date'] = '12/12/1994'
    return patient


def get_locality(dict=False, form=False):
    locality = {
        'country': 1,
        'state': 'RJ',
        'city': 'Niteroi',
        'neighborhood': 'Icarai',
        'zone': 9,
    }

    if not dict:
        locality = Locality(**locality)
    return locality
