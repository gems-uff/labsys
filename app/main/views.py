import datetime

from flask import (
    render_template, session, redirect, url_for, current_app, flash, request,
    abort,
)
from flask_login import login_required

from .. import db
from ..models import (
    User,
    Admission,
    Patient, Address,
    Vaccine, Hospitalization, UTIHospitalization, ClinicalEvolution,
    Symptom, ObservedSymptom,
    Sample, Method, CdcExam,
)
from . import main
from .forms import NameForm, AdmissionForm, VaccineForm


IGNORED = 9
TRUE = 1
FALSE = 0


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/admissions', methods=['GET'])
def list_admissions():
    admissions = Admission.query.all()
    return render_template('list-admissions.html', admissions=admissions)

def symptom_in_admission_symptoms(symptom_id, admission):
    found = None
    for obs_symptom in admission.symptoms:
        if obs_symptom.symptom.id == symptom_id:
            return obs_symptom

    return found

@main.route('/admissions/<int:id>/detail', methods=['GET', 'POST'])
@main.route('/admissions/<int:id>/edit', methods=['GET', 'POST'])
@main.route('/admissions/<int:id>', methods=['GET', 'POST'])
def edit_admission(id):
    admission = Admission.query.get_or_404(id)

    symptoms = [{'symptom_id': s.id, 'symptom_name': s.name}
                for s in Symptom.get_primary_symptoms()]
    sec_symptoms = [{'symptom_id': s.id, 'symptom_name': s.name}
                    for s in Symptom.get_secondary_symptoms()]

    for obs_symptom in admission.symptoms:
        for symptom in symptoms:
            if symptom['symptom_id'] == obs_symptom.symptom.id:
                symptom['observed'] = obs_symptom.observed
                symptom['details'] = obs_symptom.details
        for sec_symptom in sec_symptoms:
            if sec_symptom['symptom_id'] == obs_symptom.symptom.id:
                sec_symptom['observed'] = obs_symptom.observed
                sec_symptom['details'] = obs_symptom.details


    form = AdmissionForm(
        id_lvrs_intern=admission.id_lvrs_intern,
        first_symptoms_date=admission.first_symptoms_date,
        semepi_symptom=admission.semepi_symptom,
        state_id=admission.state_id,
        city_id=admission.city_id,
        health_unit=admission.health_unit,
        requesting_institution=admission.requesting_institution,
        details=admission.details,
        patient=admission.patient,
        vaccine=admission.vaccine,
        hospitalization=admission.hospitalization,
        uti_hospitalization=admission.uti_hospitalization,
        clinical_evolution=admission.clinical_evolution,
        symptoms=symptoms,
        sec_symptoms=sec_symptoms,
        samples=admission.samples,
    )
    form.submit.label.text = 'Editar'

    if form.validate_on_submit():
        if form.id_lvrs_intern.data != admission.id_lvrs_intern and \
                Admission.query.filter_by(
                    id_lvrs_intern=form.id_lvrs_intern.data).first() \
                    is not None:
            flash('Número Interno já cadastrado! Escolha outro!')
        else:
            admission.patient.name = form.patient.data['name']
            admission.patient.birth_date = form.patient.data['birth_date']
            admission.patient.age = form.patient.data['age']
            admission.patient.age_unit = form.patient.data['age_unit']
            admission.patient.gender = form.patient.data['gender']

            admission.patient.residence.country_id = form.patient.residence.data['country_id']\
                if form.patient.residence.data['country_id'] is not -1 else None
            admission.patient.residence.state_id = form.patient.residence.data['state_id']\
                if form.patient.residence.data['state_id'] is not -1 else None
            admission.patient.residence.city_id = form.patient.residence.data['city_id']\
                if form.patient.residence.data['city_id'] is not -1 else None
            admission.patient.residence.neighborhood = form.patient.residence.data['neighborhood']
            admission.patient.residence.zone = form.patient.residence.data['zone']
            admission.patient.residence.details = form.patient.residence.data['details']

            admission.id_lvrs_intern = form.id_lvrs_intern.data
            admission.first_symptoms_date = form.first_symptoms_date.data
            admission.semepi_symptom = form.semepi_symptom.data
            admission.state_id = form.state_id.data \
                if form.state_id.data is not -1 else None
            admission.city_id = form.city_id.data \
                if form.city_id.data is not -1 else None
            admission.health_unit = form.health_unit.data
            admission.requesting_institution = form.requesting_institution.data
            admission.details = form.details.data

            if form.vaccine.data['applied'] is not IGNORED:
                admission.vaccine.applied = bool(form.vaccine.data['applied'])
                admission.vaccine.last_dose_date = \
                    form.vaccine.data['last_dose_date']
            else:
                admission.vaccine = None

            if form.hospitalization.data['occurred'] is not IGNORED:
                admission.hospitalization.occurred = \
                    bool(form.hospitalization.data['occurred'])
                admission.hospitalization.date = form.hospitalization.data['date']
            else:
                admission.hospitalization = None

            if form.uti_hospitalization.data['occurred'] is not IGNORED:
                admission.uti_hospitalization.occurred = \
                    bool(form.uti_hospitalization.data['occurred'])
                admission.uti_hospitalization.date = \
                    form.uti_hospitalization.data['date']
            else:
                admission.uti_hospitalization = None

            if form.clinical_evolution.data['death'] is not IGNORED:
                admission.clinical_evolution.death = \
                    bool(form.clinical_evolution.data['death'])
                admission.clinical_evolution.date = \
                    form.clinical_evolution.data['date']
            else:
                admission.clinical_evolution = None

            for symptom_form in form.symptoms:
                observed = symptom_in_admission_symptoms(
                    symptom_form['symptom_id'], admission)
                if observed is None:
                    if symptom_form.data['observed'] is not IGNORED:
                        observed = ObservedSymptom(
                            observed=bool(symptom_form.data['observed']),
                            details=symptom_form.data['details'],
                            symptom_id=symptom_form.data['symptom_id'],
                            admission=admission,
                        )
                else:
                    os = ObservedSymptom.query.get(observed.id)
                    if symptom_form.data['observed'] is IGNORED:
                        db.session.delete(os)
                    else:
                        os.observed = bool(symptom_form.data['observed'])
                        os.details = symptom_form.data['details']
                        db.session.add(os)

            for symptom_form in form.sec_symptoms:
                observed = symptom_in_admission_symptoms(
                    symptom_form['symptom_id'], admission)
                if observed is None:
                    if symptom_form.data['observed'] is not IGNORED:
                        observed = ObservedSymptom(
                            observed=bool(symptom_form.data['observed']),
                            details=symptom_form.data['details'],
                            symptom_id=symptom_form.data['symptom_id'],
                            admission=admission,
                        )
                else:
                    os = ObservedSymptom.query.get(observed.id)
                    if symptom_form.data['observed'] is IGNORED:
                        db.session.delete(os)
                    else:
                        os.observed = bool(symptom_form.data['observed'])
                        os.details = symptom_form.data['details']
                        db.session.add(os)

            for sample_form in form.samples:
                sample = admission.samples.first()
                sample.admission_date = sample_form.data['admission_date']
                sample.collection_date = sample_form.data['collection_date']
                sample.semepi = sample_form.data['semepi']
                sample.method_id = sample_form.data['method_id'] \
                    if sample_form.data['method_id'] is not -1 else None
                sample_form.cdc_exam.form.populate_obj(sample.cdc_exam)
                    # flu_type=sample_form.cdc_exam.data['flu_type'],
                    # flu_subtype=sample_form.cdc_exam.data['flu_subtype'],
                    # dominant_ct=sample_form.cdc_exam.data['dominant_ct'],
                    # details=sample_form.cdc_exam.data['details'],
                    # sample=sample,
                # )

            db.session.add(admission)
            flash('Admissão editada com sucesso!')
        return redirect(url_for('main.edit_admission', id=admission.id))

    return render_template('create-admission.html', form=form)


@main.route('/admissions/<int:id>/delete', methods=['GET'])
def delete_admission(id):
    admission = Admission.query.get(id)
    if admission is None:
        flash('Admissão com esse id não existe.')
        abort(404)
    return ('Delete not implemented yet.')


@main.route('/admissions/create', methods=['GET', 'POST'])
def create_admission():
    form = AdmissionForm(
        symptoms=[{'symptom_id': s.id, 'symptom_name': s.name}
                  for s in Symptom.get_primary_symptoms()],
        sec_symptoms=[{'symptom_id': s.id, 'symptom_name': s.name}
                      for s in Symptom.get_secondary_symptoms()],
    )

    # POST and valid
    if form.validate_on_submit():
        admission = Admission.query.filter_by(
            id_lvrs_intern=form.id_lvrs_intern.data).first()
        if admission is None:
            patient = Patient(
                name=form.patient.data['name'],
                birth_date=form.patient.data['birth_date'],
                age=form.patient.data['age'],
                age_unit=form.patient.data['age_unit'],
                gender=form.patient.data['gender'],
            )

            patient_residence = Address(
                patient=patient,
                country_id = form.patient.residence.data['country_id']
                    if form.patient.residence.data['country_id'] is not -1 else None,
                state_id=form.patient.residence.data['state_id']
                    if form.patient.residence.data['state_id'] is not -1 else None,
                city_id=form.patient.residence.data['city_id']
                    if form.patient.residence.data['city_id'] is not -1 else None,
                neighborhood=form.patient.residence.data['neighborhood'],
                zone=form.patient.residence.data['zone'],
                details=form.patient.residence.data['details']
            )

            admission = Admission(
                id_lvrs_intern=form.id_lvrs_intern.data,
                first_symptoms_date=form.first_symptoms_date.data,
                semepi_symptom=form.semepi_symptom.data,
                state_id=form.state_id.data
                    if form.state_id.data is not -1 else None,
                city_id=form.city_id.data
                    if form.city_id.data is not -1 else None,
                health_unit=form.health_unit.data,
                requesting_institution=form.requesting_institution.data,
                details=form.details.data,
                patient=patient,
            )

            if form.vaccine.data['applied'] is not IGNORED:
                Vaccine(
                    applied=bool(form.vaccine.data['applied']),
                    last_dose_date=form.vaccine.data['last_dose_date'],
                    admission=admission,
                )

            if form.hospitalization.data['occurred'] is not IGNORED:
                Hospitalization(
                    occurred=bool(form.hospitalization.data['occurred']),
                    date=form.hospitalization.data['date'],
                    admission=admission,
                )

            if form.uti_hospitalization.data['occurred'] is not IGNORED:
                UTIHospitalization(
                    occurred=bool(form.uti_hospitalization.data['occurred']),
                    date=form.uti_hospitalization.data['date'],
                    admission=admission,
                )

            if form.clinical_evolution.data['death'] is not IGNORED:
                ClinicalEvolution(
                    death=bool(form.clinical_evolution.data['death']),
                    date=form.vaccine.data['date'],
                    admission=admission,
                )

            for symptom_form in form.symptoms:
                if symptom_form.data['observed'] is not IGNORED:
                    ObservedSymptom(
                        observed=bool(symptom_form.data['observed']),
                        details=symptom_form.data['details'],
                        symptom_id=symptom_form.data['symptom_id'],
                        admission=admission,
                    )

            for sec_symptom_form in form.sec_symptoms:
                if sec_symptom_form.data['observed'] is True:
                    ObservedSymptom(
                        observed=True,
                        details=sec_symptom_form.data['details'],
                        symptom_id=sec_symptom_form.data['symptom_id'],
                        admission=admission,
                    )

            for sample_form in form.samples:
                sample = Sample(
                    admission_date=sample_form.data['admission_date'],
                    collection_date=sample_form.data['collection_date'],
                    semepi=sample_form.data['semepi'],
                    method_id=sample_form.data['method_id']
                        if sample_form.data['method_id'] is not -1 else None,
                    admission=admission,
                )
                CdcExam(
                    flu_type=sample_form.cdc_exam.data['flu_type'],
                    flu_subtype=sample_form.cdc_exam.data['flu_subtype'],
                    dominant_ct=sample_form.cdc_exam.data['dominant_ct'],
                    details=sample_form.cdc_exam.data['details'],
                    sample=sample,
                )

            db.session.add(admission)
            flash('Admissão criada com sucesso!')
        else:
            flash('Número Interno já cadastrado! Escolha outro!')
        return redirect(url_for('.create_admission'))

    return render_template('create-admission.html', form=form,)
