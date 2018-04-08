from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import login_required

from labsys.auth.decorators import permission_required
from labsys.auth.models import Permission

from . import blueprint
from ..extensions import db
from .forms import AdmissionForm
from .models import (Address, Admission, CdcExam, ClinicalEvolution,
                     Hospitalization, ObservedSymptom, Patient, Sample,
                     Symptom, UTIHospitalization, Vaccine)

IGNORED = 9
TRUE = 1
FALSE = 0


# TODO: do I need this?
@blueprint.app_context_processor
def inject_permissions():
    """This function is executed each request,
    even though outside of the bluprint"""
    return dict(Permission=Permission)


@blueprint.route('/', methods=['GET'])
@permission_required(Permission.VIEW)
def list_admissions():
    admissions = Admission.query.all()
    return render_template('admissions/list-admissions.html', admissions=admissions)


def symptom_in_admission_symptoms(symptom_id, admission):
    found = None
    for obs_symptom in admission.symptoms.all():
        if obs_symptom.symptom_id == symptom_id:
            return obs_symptom
    return found


def get_symptoms(admission_id):
    query = 'SELECT s.id, s.name, s.primary, obs.observed, obs.details \
        FROM symptoms s \
        LEFT JOIN observed_symptoms obs \
            ON s.id = obs.symptom_id \
        WHERE obs.admission_id = %d OR obs.admission_id IS NULL' % admission_id
    result = db.engine.execute(query)

    mapped_symptoms = [
        {
            'symptom_id': symptom[0],
            'symptom_name': symptom[1],
            'primary': symptom[2],
            'observed': symptom[3],
            'details': symptom[4],
        } for symptom in result.fetchall()]
    return mapped_symptoms

@blueprint.route('/<int:id>', methods=['GET', 'POST'])
@permission_required(Permission.VIEW)
def detail_admission(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    symptoms = get_symptoms(admission_id)
    primary_symptoms = []
    sec_symptoms = []
    for symptom in symptoms:
        if symptom.primary:
            primary_symptoms.append(symptom)
        else:
            sec_symptoms.append(symptom)

    form = AdmissionForm(
        id_lvrs_intern=admission.id_lvrs_intern,
        first_symptoms_date=admission.first_symptoms_date,
        semepi_symptom=admission.semepi_symptom,
        state=admission.state,
        city=admission.city,
        health_unit=admission.health_unit,
        requesting_institution=admission.requesting_institution,
        details=admission.details,
        patient=admission.patient,
        vaccine=admission.vaccine,
        hospitalization=admission.hospitalization,
        uti_hospitalization=admission.uti_hospitalization,
        clinical_evolution=admission.clinical_evolution,
        symptoms=primary_symptoms,
        sec_symptoms=sec_symptoms,
        samples=admission.samples, )

    return render_template('admissions/create-admission.html', form=form, edit=False)


@blueprint.route('/<int:id>/edit', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def edit_admission(id):
    admission = Admission.query.get_or_404(id)

    symptoms = [{
        'symptom_id': s.id,
        'symptom_name': s.name
    } for s in Symptom.get_primary()]
    sec_symptoms = [{
        'symptom_id': s.id,
        'symptom_name': s.name
    } for s in Symptom.get_secondary()]

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
        state=admission.state,
        city=admission.city,
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
        samples=admission.samples, )
    form.submit.label.text = 'Editar'

    if form.validate_on_submit():
        if form.id_lvrs_intern.data != admission.id_lvrs_intern and \
                Admission.query.filter_by(id_lvrs_intern=form.id_lvrs_intern.data).first() is not None:
            flash('Número Interno já cadastrado! Escolha outro!', 'danger')
        else:
            admission.patient.name = form.patient.data['name']
            admission.patient.birth_date = form.patient.data['birth_date']
            admission.patient.age = form.patient.data['age']
            admission.patient.age_unit = form.patient.data['age_unit']
            admission.patient.gender = form.patient.data['gender']

            # TODO: probably override fields to allow returning None (ignoring coercion?)
            admission.patient.residence.country = form.patient.residence.data['country']\
                if form.patient.residence.data['country'] is not -1 else None
            admission.patient.residence.state = form.patient.residence.data['state']\
                if form.patient.residence.data['state'] is not -1 else None
            admission.patient.residence.city = form.patient.residence.data['city']\
                if form.patient.residence.data['city'] is not -1 else None
            admission.patient.residence.neighborhood = form.patient.residence.data[
                'neighborhood']
            admission.patient.residence.zone = form.patient.residence.data[
                'zone']
            admission.patient.residence.details = form.patient.residence.data[
                'details']

            admission.id_lvrs_intern = form.id_lvrs_intern.data
            admission.first_symptoms_date = form.first_symptoms_date.data
            admission.semepi_symptom = form.semepi_symptom.data
            admission.state = form.state.data \
                if form.state.data is not -1 else None
            admission.city = form.city.data \
                if form.city.data is not -1 else None
            admission.health_unit = form.health_unit.data
            admission.requesting_institution = form.requesting_institution.data
            admission.details = form.details.data

            # TODO: single fks must not use the ignored=>not saved logic
            if form.vaccine.data['applied'] is not IGNORED:
                admission.vaccine.applied = bool(form.vaccine.data['applied'])
                admission.vaccine.last_dose_date = \
                    form.vaccine.data['last_dose_date']
            else:
                admission.vaccine = None

            if form.hospitalization.data['occurred'] is not IGNORED:
                admission.hospitalization.occurred = \
                    bool(form.hospitalization.data['occurred'])
                admission.hospitalization.date = form.hospitalization.data[
                    'date']
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
                    symptom_form.data['symptom_id'], admission)
                if observed is None:
                    if symptom_form.data['observed'] is not IGNORED:
                        ObservedSymptom(
                            observed=bool(symptom_form.data['observed']),
                            details=symptom_form.data['details'],
                            symptom_id=symptom_form.data['symptom_id'],
                            admission=admission)
                else:
                    os = ObservedSymptom.query.get(observed.id)
                    if symptom_form.data['observed'] is IGNORED:
                        db.session.delete(os)
                    else:
                        os.observed = bool(symptom_form.data['observed'])
                        os.details = symptom_form.data['details']
                        db.session.add(os)

            for sec_symptom_form in form.sec_symptoms:
                observed = symptom_in_admission_symptoms(
                    sec_symptom_form.data['symptom_id'], admission)
                if observed is None:
                    if sec_symptom_form.data['observed'] is True:
                        ObservedSymptom(
                            observed=sec_symptom_form.data['observed'],
                            details=sec_symptom_form.data['details'],
                            symptom_id=sec_symptom_form.data['symptom_id'],
                            admission=admission)
                else:
                    os = ObservedSymptom.query.get(observed.id)
                    if sec_symptom_form.data['observed'] is False:
                        db.session.delete(os)
                    else:
                        os.observed = sec_symptom_form.data['observed']
                        os.details = sec_symptom_form.data['details']
                        db.session.add(os)

            index = 0
            for sample_form in form.samples.entries:
                sample = admission.samples[index]
                print(sample)
                if sample is not None:
                    sample.admission_date = sample_form.data['admission_date']
                    sample.collection_date = sample_form.data[
                        'collection_date']
                    sample.semepi = sample_form.data['semepi']
                    sample.details = sample_form.data['details']
                    sample.method_id = sample_form.data[
                        'method_id'] if sample_form.data['method_id'] is not -1 else None
                    sample_form.cdc_exam.form.populate_obj(sample.cdc_exam)
                    print(sample.cdc_exam)
                index += 1

            db.session.add(admission)
            flash('Admissão editada com sucesso!', 'success')
        return redirect(url_for('admissions.edit_admission', id=admission.id))

    return render_template('admissions/create-admission.html', form=form)


@blueprint.route('/<int:id>/delete', methods=['GET'])
@login_required
@permission_required(Permission.DELETE)
def delete_admission(id):
    admission = Admission.query.get(id)
    if admission is None:
        flash('Admissão com esse id não existe.', 'danger')
        abort(404)
    return ('Delete not implemented yet.')


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.CREATE)
def create_admission():
    form = AdmissionForm(
        symptoms=[{
            'symptom_id': s.id,
            'symptom_name': s.name
        } for s in Symptom.get_primary()],
        sec_symptoms=[{
            'symptom_id': s.id,
            'symptom_name': s.name
        } for s in Symptom.get_secondary()], )

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
                gender=form.patient.data['gender'], )

            Address(
                patient=patient,
                country=form.patient.residence.data['country'] if
                form.patient.residence.data['country'] is not -1 else None,
                state=form.patient.residence.data['state']
                if form.patient.residence.data['state'] is not -1 else None,
                city=form.patient.residence.data['city']
                if form.patient.residence.data['city'] is not -1 else None,
                neighborhood=form.patient.residence.data['neighborhood'],
                zone=form.patient.residence.data['zone'],
                details=form.patient.residence.data['details'])

            admission = Admission(
                id_lvrs_intern=form.id_lvrs_intern.data,
                first_symptoms_date=form.first_symptoms_date.data,
                semepi_symptom=form.semepi_symptom.data,
                state=form.state.data
                if form.state.data is not -1 else None,
                city=form.city.data
                if form.city.data is not -1 else None,
                health_unit=form.health_unit.data,
                requesting_institution=form.requesting_institution.data,
                details=form.details.data,
                patient=patient, )

            if form.vaccine.data['applied'] is not IGNORED:
                Vaccine(
                    applied=bool(form.vaccine.data['applied']),
                    last_dose_date=form.vaccine.data['last_dose_date'],
                    admission=admission, )

            if form.hospitalization.data['occurred'] is not IGNORED:
                Hospitalization(
                    occurred=bool(form.hospitalization.data['occurred']),
                    date=form.hospitalization.data['date'],
                    admission=admission, )

            if form.uti_hospitalization.data['occurred'] is not IGNORED:
                UTIHospitalization(
                    occurred=bool(form.uti_hospitalization.data['occurred']),
                    date=form.uti_hospitalization.data['date'],
                    admission=admission, )

            if form.clinical_evolution.data['death'] is not IGNORED:
                ClinicalEvolution(
                    death=bool(form.clinical_evolution.data['death']),
                    date=form.vaccine.data['date'],
                    admission=admission, )

            for symptom_form in form.symptoms:
                if symptom_form.data['observed'] is not IGNORED:
                    ObservedSymptom(
                        observed=bool(symptom_form.data['observed']),
                        details=symptom_form.data['details'],
                        symptom_id=symptom_form.data['symptom_id'],
                        admission=admission, )

            for sec_symptom_form in form.sec_symptoms:
                if sec_symptom_form.data['observed'] is True:
                    ObservedSymptom(
                        observed=True,
                        details=sec_symptom_form.data['details'],
                        symptom_id=sec_symptom_form.data['symptom_id'],
                        admission=admission, )

            for sample_form in form.samples:
                sample = Sample(
                    admission_date=sample_form.data['admission_date'],
                    collection_date=sample_form.data['collection_date'],
                    semepi=sample_form.data['semepi'],
                    details=sample_form.data['details'],
                    method_id=sample_form.data['method_id']
                    if sample_form.data['method_id'] is not -1 else None,
                    admission=admission, )
                CdcExam(
                    flu_type=sample_form.cdc_exam.data['flu_type'],
                    flu_subtype=sample_form.cdc_exam.data['flu_subtype'],
                    dominant_ct=sample_form.cdc_exam.data['dominant_ct'],
                    details=sample_form.cdc_exam.data['details'],
                    sample=sample, )

            db.session.add(admission)
            flash('Admissão criada com sucesso!', 'success')
        else:
            flash('Número Interno já cadastrado! Escolha outro!', 'danger')
        return redirect(url_for('.create_admission'))

    return render_template(
        'admissions/create-admission.html',
        form=form, )
