import csv, sys

from labsys.admissions.models import Admission, Patient, Address

attributes_map = {
    # csv name => Class.attribute
    'Requisição': Admission.gal_request,
    'Unidade Soicitante': Admission.requesting_institution,
    'Municipio do Solicitante': Admission.city,
    'Estado do Solicitante': Admission.state,
    'Data do 1º Sintomas': Admission.first_symptoms_date,
    # 'Data da Coleta': Admission.samples[0].collection_date, Not yet. Handling multiple samples is still hard
    # 'Data do Recebimento': ... Same issue as above.
    'Paciente': Patient.name,
    'Data de Nascimento': Patient.birth_date,
    'Idade': Patient.age,
    'Tipo Idade': Patient.age_unit, # Must be converted from CSV
    'Sexo': Patient.gender,
    'Bairro': Address.neighborhood,
    'Municipio de Residência': Address.city,
    'Estado de Residência': Address.state,
    'País de Residência': Address.country,
    'Zona': Address.zone, # Must be converted from CSV
}

file_name = sys.argv[1]

lines = []
print(file_name)

with open(file_name, newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        lines.append(row)

print(lines[0])
