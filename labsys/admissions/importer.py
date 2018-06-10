import csv

import psycopg2
from flask import flash

from labsys.extensions import db

from . import logger, service
from .models import Address, Admission, Patient


def insert_admission(admission):
    query_admission = Admission.query.filter_by(
        id_lvrs_intern=admission.id_lvrs_intern).first()
    if query_admission:
        # logger.info(f'{admission.id_lvrs_intern} already exists.')
        flash(f'{admission.id_lvrs_intern} já existe no banco', 'warning')
        return
    try:
        db.session.add(admission)
        db.session.commit()
        # logger.info(f'{admission.id_lvrs_intern} inserted')
    except psycopg2.DataError as pg_error:
        print('Psycopg2!')
        print(pg_error)
    except Exception as exc:
        print('Generic exception')
        print(exc)


def create_models_from_csv(file_path):
    file_path = '/home/gcrsaldanha/Repositories/labsys/gal.csv'
    try:
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar=r'"')
            curr_request_number = None
            for csv_row in csv_reader:
                if csv_row['Requisição'] != curr_request_number:
                    curr_request_number = csv_row['Requisição']
                    patient = Patient.model_from_csv(csv_row)
                    address = Address.model_from_csv(csv_row)
                    admission = Admission.model_from_csv(csv_row)
                    patient.addess = address
                    admission.patient = patient
                    service.insert_admission(admission)
    except FileNotFoundError as not_found:
        print('File not found!!')
        print(not_found)
