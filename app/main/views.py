from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import (
    User,
    Admission,
    Patient,
    Vaccine, Hospitalization, UTIHospitalization, ClinicalEvolution,
    Symptom, ObservedSymptom,
    Sample, Method, CdcExam,
)
from . import main
from .forms import NameForm, AdmissionForm, SymptomForm


def get_method_choices():
    return [(m.id, m.name) for m in Method.query.all()]


NONE = 9
TRUE = 1
FALSE = 0


@main.route('/admissions/create', methods=['GET', 'POST'])
def create_admission():
    form = AdmissionForm(
        symptoms=[{'symptom_id': s.id, 'symptom_name': s.name}
                  for s in Symptom.get_primary_symptoms()],
        sec_symptoms=[{'symptom_id': s.id, 'symptom_name': s.name}
                      for s in Symptom.get_secondary_symptoms()],
    )
    # Set sample method choices (error if not set, move to constructor later)
    for sample_form in form.samples.entries:
        sample_form.method.choices = get_method_choices()

    # POST and valid
    if form.validate_on_submit():
        admission = Admission.query.filter_by(
            id_lvrs_intern=form.id_lvrs_intern.data).first()
        if admission is None:
            patient = Patient(name=form.patient.data['name'])

            admission = Admission(
                id_lvrs_intern=form.id_lvrs_intern.data,
                patient=patient,
            )

            if form.vaccine.data['occurred'] is not NONE:
                Vaccine(
                    applied=bool(form.vaccine.data['occurred']),
                    last_dose_date=form.vaccine.data['date'],
                    admission=admission,
                )

            if form.hospitalization.data['occurred'] is not NONE:
                Hospitalization(
                    occurred=bool(form.hospitalization.data['occurred']),
                    date=form.hospitalization.data['date'],
                    admission=admission,
                )

            if form.uti_hospitalization.data['occurred'] is not NONE:
                UTIHospitalization(
                    occurred=bool(form.uti_hospitalization.data['occurred']),
                    date=form.uti_hospitalization.data['date'],
                    admission=admission,
                )

            if form.clinical_evolution.data['occurred'] is not NONE:
                ClinicalEvolution(
                    death=bool(form.clinical_evolution.data['occurred']),
                    date=form.vaccine.data['date'],
                    admission=admission,
                )

            for symptom_form in form.symptoms:
                if symptom_form.data['observed'] is not NONE:
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
                    collection_date=sample_form.data['collection_date'],
                    method_id=sample_form.data['method'],
                    admission=admission,
                )
                CdcExam(
                    details=sample_form.cdc_exam.data['details'],
                    sample=sample,
                )

            db.session.add(admission)
        else:
            print('DUPLICATE ADMISSION FLASH')
        return redirect(url_for('.create_admission'))
    return render_template('create-admission.html', form=form,)
