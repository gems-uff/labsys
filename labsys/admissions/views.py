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


# TODO: find out why when fail it creates another instance of fields
@blueprint.route('/<int:admission_id>/symptoms', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_symptoms(admission_id):
    template = 'admissions/formlist.html'
    admission = Admission.query.get_or_404(admission_id)
    symptoms = get_admission_symptoms(admission.id)
    prime_symptoms = [
        symptom for symptom in symptoms if symptom['primary'] is True]
    sec_symptoms = [
        symptom for symptom in symptoms if symptom['primary'] is False]
    form = forms.ObservedEntityFormList(data={'primary': prime_symptoms, 'secondary': sec_symptoms})
    if form.validate_on_submit():
        for prime_symptom in form.primary.entries:
            if prime_symptom.observed.data is not None:
                print(prime_symptom.entity_id.data)
                print(prime_symptom.observed.data)
                print(prime_symptom.details.data)
        return redirect(url_for('.add_symptoms', admission_id=admission_id))
    return render_template(template, form=form)
