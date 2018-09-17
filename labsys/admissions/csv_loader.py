import csv
import builtins

from flask import flash

from labsys.extensions import db

from . import service, logger
from .models import Address, Admission, Patient


def insert_admission(admission):
    query_admission = Admission.query.filter_by(
        id_lvrs_intern=admission.id_lvrs_intern).first()
    if query_admission:
        logger.warning(f'{admission.id_lvrs_intern} already exists.')
        flash(f'Uma admissão com o número {admission.id_lvrs_intern} \
            já existe no banco', 'warning')
        return
    try:
        db.session.add(admission)
        db.session.commit()
        logger.info(f'{admission.id_lvrs_intern} inserted')
    except Exception as exc:
        logger.error(f'Inserting {admission.id_lvrs_intern} excepted')
        db.session.rollback()


def create_models_from_csv(file_path):
    try:
        with open(file_path, 'r', newline='', encoding='cp1252') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=';', quotechar=r'"')
            curr_request_number = None
            inserted_amount = 0
            for csv_row in csv_reader:
                if csv_row['Requisição'] != curr_request_number:
                    curr_request_number = csv_row['Requisição']
                    patient = Patient.model_from_csv(csv_row)
                    address = Address.model_from_csv(csv_row)
                    admission = Admission.model_from_csv(csv_row)
                    patient.residence = address
                    admission.patient = patient
                    service.insert_admission(admission)
                    # TODO: check if it was really inserted because it could be a duplicate
                    inserted_amount += 1
            flash(f'{inserted_amount} admissões inseridas.', 'success')
    except builtins.UnicodeDecodeError as uniDecError:
        logger.error(f'UnicodeDecodeError: {uniDecError}')
        flash('Erro de formato no arquivo do GAL, contate um administrador.', 'danger')
    except FileNotFoundError:
        flash(f'O arquivo {file_path} não existe', 'danger')
