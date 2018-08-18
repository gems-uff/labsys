from flask import flash, redirect, render_template, url_for, session

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
    even though outside of the blueprint'''
    return dict(Permission=Permission)


@blueprint.context_processor
def inject_sidebar_links():
    admission_id = session.get('admission_id', 1)
    admission_link = url_for('.detail_admission', admission_id=admission_id)
    symptoms_link = url_for('.add_symptoms', admission_id=admission_id)
    risk_factors_link = url_for('.add_risk_factors', admission_id=admission_id)
    dated_events_link = url_for('.add_dated_events', admission_id=admission_id)
    antiviral_link = url_for('.add_antiviral', admission_id=admission_id)
    xray_link = url_for('.add_xray', admission_id=admission_id)
    samples_link = url_for('.add_sample', admission_id=admission_id)
    sidebar_links = {
        'Admissão e Paciente': admission_link,
        'Sintomas': symptoms_link,
        'Fatores de risco': risk_factors_link,
        'Vacinação, Hospitalização e Óbito': dated_events_link,
        'Uso de antiviral': antiviral_link,
        'Raio X de Tórax': xray_link,
        'Amostras coletadas': samples_link,
    }
    return {'sidebar_links': sidebar_links}


@blueprint.route('/', methods=['GET'])
@permission_required(Permission.VIEW)
def list_admissions():
    template = 'admissions/list-admissions.html'
    view = 'admissions.list_admissions'
    query = Admission.query.order_by(Admission.id_lvrs_intern)
    context_title = 'admissions'
    return paginated(
        query=query,
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
            return redirect(url_for('.create_admission'))
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
        return redirect(
            url_for('.detail_admission', admission_id=admission.id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>', methods=['GET', 'POST'])
@permission_required(Permission.VIEW)
def detail_admission(admission_id):
    session['admission_id'] = admission_id
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/detail-admission.html'
    admission_form = AdmissionForm(obj=admission)
    if admission_form.validate_on_submit():
        query_admission = Admission.query.filter_by(
            id_lvrs_intern=admission_form.id_lvrs_intern.data).first()
        if query_admission is not None and query_admission.id != admission.id:
            flash('Número Interno já cadastrado!', 'danger')
        else:
            service.upsert_admission(admission, admission_form)
            flash('Admissão atualizada com sucesso', 'success')
        return redirect(
            url_for('.detail_admission', admission_id=admission.id))
    return render_template(
        template,
        admission=admission_form,
    )


@blueprint.route('/<int:admission_id>/dated-events', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_dated_events(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/dated-events.html'
    dated_events = service.get_dated_events(admission)
    form = forms.DatedEventFormGroup(data=dated_events)
    if form.validate_on_submit():
        service.upsert_dated_events(admission, form.data)
        return redirect(
            url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/symptoms', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_symptoms(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/entities_formlist.html'
    symptoms, symptoms_dict = service.get_admission_symptoms(admission_id)
    form = forms.ObservedSymptomFormList(
        data={
            'primary': symptoms_dict,
            'secondary': admission.secondary_symptoms,
        })
    if form.validate_on_submit():
        admission.secondary_symptoms = form.secondary.data
        for symptom in form.primary.entries:
            service.upsert_symptom(admission_id, symptom.data)
        return redirect(
            url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/riskfactors', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_risk_factors(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/entities_formlist.html'
    risk_factors, risk_factors_dict = service.get_admission_risk_factors(
        admission_id)
    form = forms.ObservedRiskFactorFormList(
        data={
            'primary': risk_factors_dict,
            'secondary': admission.secondary_risk_factors,
        })
    if form.validate_on_submit():
        admission.secondary_risk_factors = form.secondary.data
        for risk_factor in form.primary.entries:
            service.upsert_risk_factor(admission_id, risk_factor.data)
        return redirect(
            url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/antiviral', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_antiviral(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/antiviral.html'
    antiviral_formdata = service.get_antiviral(admission)
    form = forms.AntiviralForm(data=antiviral_formdata)
    if form.validate_on_submit():
        service.upsert_antiviral(admission, form.data)
        return redirect(
            url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/xray', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_xray(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/xray.html'
    xray_formdata = service.get_xray(admission)
    form = forms.XRayForm(data=xray_formdata)
    if form.validate_on_submit():
        service.upsert_xray(admission, form.data)
        return redirect(
            url_for('.detail_admission', admission_id=admission_id))
    return render_template(template, form=form)


@blueprint.route('/<int:admission_id>/samples', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def add_sample(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    template = 'admissions/samples.html'
    samples = service.get_samples(admission)
    form = forms.SampleForm()
    if form.validate_on_submit():
        service.add_sample(admission, form)
        return redirect(url_for('.add_sample', admission_id=admission_id))
    return render_template(
        template,
        form=form,
        samples=samples,
        admission_link=url_for('.detail_admission', admission_id=admission_id))


@blueprint.route('/samples/<int:sample_id>', methods=['GET', 'POST'])
@permission_required(Permission.CREATE)
def edit_sample(sample_id):
    sample = Sample.query.get_or_404(sample_id)
    # TODO: find out why dates why weird years are not loaded correctly
    template = 'admissions/sample.html'
    form = forms.SampleForm(obj=sample)
    form.submit.label.text = 'Salvar edição'
    if form.validate_on_submit():
        service.update_sample(sample, form)
        return redirect(
            url_for('.add_sample', admission_id=sample.admission_id))
    return render_template(
        template,
        form=form,
        sample=sample,
        add_sample_link=url_for(
            '.add_sample', admission_id=sample.admission_id))
