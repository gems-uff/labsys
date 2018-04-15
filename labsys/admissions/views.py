from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from labsys.auth.decorators import permission_required
from labsys.auth.models import Permission
from labsys.utils.decorators import paginated

from . import blueprint
from ..extensions import db
from .forms import AdmissionForm
from . import forms
from .models import (Address, Admission, CdcExam, ClinicalEvolution,
                     Hospitalization, ObservedSymptom, Patient, Sample,
                     Symptom, UTIHospitalization, Vaccine)
from .services import get_admission_risk_factors, get_admission_symptoms


# TODO: do I need this?
@blueprint.app_context_processor
def inject_permissions():
    '''This function is executed each request,
    even though outside of the bluprint'''
    return dict(Permission=Permission)


@blueprint.route('/', methods=['GET'])
@permission_required(Permission.VIEW)
def list_admissions():
    template = 'admissions/list-admissions.html'
    view = 'admissions.list_admissions'
    query = Admission.query.order_by(Admission.id_lvrs_intern)
    context_title = 'admissions'
    return paginated(query=query,
                     template_name=template,
                     view_method=view,
                     context_title=context_title)


@blueprint.route('/create', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def create_admission():
    form = AdmissionForm()
    template = 'admissions/create-admission.html'
    if form.validate_on_submit():
        admission = Admission.query.filter_by(
            id_lvrs_intern=form.id_lvrs_intern.data).first()
        if admission is not None:
            flash('Número Interno já cadastrado!', 'danger')
        else:
            # Unfortunately I cannot use **form.data to create an instance nor populate_obj
            # because of nesting
            patient = Patient(
                name=form.patient.data['name'],
                birth_date=form.patient.data['birth_date'],
                age=form.patient.data['age'],
                age_unit=form.patient.data['age_unit'],
                gender=form.patient.data['gender'],
            )
            patient.residence = Address(
                **form.patient.form.residence.form.data)
            admission = Admission(
                patient=patient,
                id_lvrs_intern=form.id_lvrs_intern.data,
                first_symptoms_date=form.first_symptoms_date.data,
                semepi_symptom=form.semepi_symptom.data,
                state=form.state.data,
                city=form.city.data,
                health_unit=form.health_unit.data,
                requesting_institution=form.requesting_institution.data,
                details=form.details.data,
            )

            db.session.add(admission)
            db.session.commit()
            flash('Admissão criada com sucesso!', 'success')
        return redirect(url_for('.detail_admission',
                                admission_id=admission.id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>', methods=['GET'])
@permission_required(Permission.VIEW)
def detail_admission(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    admission_form = AdmissionForm(obj=admission)
    return render_template('admissions/detail-admission.html',
                           admission=admission_form)


@blueprint.route('/<int:admission_id>/dated-events', methods=['GET, POST'])
@permission_required(Permission.CREATE)
def add_dated_events(admission_id):
    vaccine_form = forms.VaccineForm(occurred=1, date='2018-0101')


@blueprint.route('/test-symptoms-formlist')
def test_symptoms_formlist():
    template = 'admissions/formlist.html'
    prime_symptoms = [
        {'entity_id': 1, 'observed': True, 'details': 'details', 'entity_name': 'Febre'},
        {'entity_id': 2, 'observed': False, 'details': '', 'entity_name': 'Gripe'},
        {'entity_id': 3, 'observed': None},
    ]
    sec_symptoms = [
        {'entity_id': 10, 'observed': True, 'details': 'aaaaaa', 'entity_name': 'dor de gargante'},
        {'entity_id': 11, 'observed': False, 'details': '', 'entity_name': 'dor de cabeca'},
    ]
    form = forms.ObservedEntityFormList(prime_entities=prime_symptoms,
                                  prime_label='Sintomas observados',
                                  sec_entities=sec_symptoms,
                                  sec_label='Sintomas secundários')
    return render_template(template,
                           form=form)


@blueprint.route('/test-riskfactors-formlist', methods=['GET', 'POST'])
def test_riskfactors_formlist():
    template = 'admissions/formlist.html'
    prime_risk_factors = [
        {'entity_id': 1, 'observed': True, 'details': 'details', 'entity_name': 'Obesidade'},
        {'entity_id': 2, 'observed': False, 'details': '', 'entity_name': 'Fator de risco qq'},
        {'entity_id': 3, 'observed': None},
    ]
    sec_risk_factors = [
        {'entity_id': 10, 'observed': True, 'details': 'aaaaaa', 'entity_name': 'fator de risco sec'},
        {'entity_id': 11, 'observed': False, 'details': '', 'entity_name': 'fator outro'},
    ]
    form = forms.ObservedEntityFormList(prime_entities=prime_risk_factors,
                                        prime_label='Fatores de Risco',
                                        sec_entities=sec_risk_factors,
                                        sec_label='Fatores de Risco secundários')
    if form.validate_on_submit():
        pass
    return render_template(template,
                           form=form)


@blueprint.route('/test-forms', methods=['POST'])
def post_test_forms():
    form = forms.ObservedEntityFormList()
    import json
    print(form.data)
    response = json.dumps(form.data)
    return response
