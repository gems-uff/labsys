from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from labsys.auth.decorators import permission_required
from labsys.auth.models import Permission
from labsys.utils.decorators import paginated
from labsys.admissions import service

from . import blueprint, forms
from ..extensions import db
from .forms import AdmissionForm
from .models import (Address, Admission, CdcExam, ClinicalEvolution,
                     Hospitalization, ObservedSymptom, Patient, Sample,
                     Symptom, UTIHospitalization, Vaccine)


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


# TODO: merge symptoms and riskfactors
@blueprint.route('/<int:admission_id>', methods=['GET'])
@permission_required(Permission.VIEW)
def detail_admission(admission_id):
    template = 'admissions/detail-admission.html'
    admission = Admission.query.get_or_404(admission_id)
    admission_form = AdmissionForm(obj=admission)
    symptoms_link = url_for('.add_symptoms', admission_id=admission_id)
    risk_factors_link = url_for('.add_risk_factors', admission_id=admission_id)
    dated_events_link = url_for('.add_dated_events', admission_id=admission_id)
    return render_template(
        template,
        admission=admission_form,
        symptoms_link=symptoms_link,
        risk_factors_link=risk_factors_link,
        dated_events_link=dated_events_link,
    )


@blueprint.route('/<int:admission_id>/dated-events', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_dated_events(admission_id):
    template = 'admissions/dated-events.html'
    admission = Admission.query.get_or_404(admission_id)
    dated_events = service.get_dated_events(admission)
    form = forms.DatedEventFormGroup(data=dated_events)
    if form.validate_on_submit():
        service.upsert_dated_events(admission, form.data)
        return redirect(url_for('.detail_admission',
                                admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/symptoms', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_symptoms(admission_id):
    template = 'admissions/entities_formlist.html'
    admission = Admission.query.get_or_404(admission_id)
    symptoms, symptoms_dict = service.get_admission_symptoms(admission_id)
    form = forms.ObservedSymptomFormList(data={
        'primary': symptoms_dict,
        'secondary': admission.secondary_symptoms,
    })
    if form.validate_on_submit():
        admission.secondary_symptoms = form.secondary.data
        for symptom in form.primary.entries:
            service.upsert_symptom(admission_id, symptom.data)
        return redirect(url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/riskfactors', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_risk_factors(admission_id):
    template = 'admissions/entities_formlist.html'
    admission = Admission.query.get_or_404(admission_id)
    risk_factors, risk_factors_dict = service.get_admission_risk_factors(admission_id)
    form = forms.ObservedRiskFactorFormList(data={
        'primary': risk_factors_dict,
        'secondary': admission.secondary_risk_factors,
    })
    if form.validate_on_submit():
        admission.secondary_risk_factors = form.secondary.data
        for risk_factor in form.primary.entries:
            service.upsert_risk_factor(admission_id, risk_factor.data)
        return redirect(url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)
