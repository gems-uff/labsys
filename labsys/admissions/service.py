import datetime
from labsys.extensions import db
from labsys.admissions.models import (
    ObservedSymptom, Admission, Symptom, RiskFactor, ObservedRiskFactor,
    Vaccine, Hospitalization, UTIHospitalization, ClinicalEvolution,
    Antiviral, XRay, Sample, CdcExam
)


def get_admission_symptoms(admission_id):
    observed_symptoms_ids = [obs.symptom_id for obs in Admission.query.get(admission_id).symptoms]
    symptoms = [s for s in Symptom.query.all()]

    mapped_symptoms = []

    for symptom in symptoms:
        if symptom.id in observed_symptoms_ids:
            observed_symptom = ObservedSymptom.query.filter_by(symptom_id=symptom.id).first()
            symptom.observed = observed_symptom.observed
            symptom.details = observed_symptom.details
        else:
            symptom.observed = None
            symptom.details = ''
        mapped_symptoms.append(symptom)
    return mapped_symptoms, [{
        'symptom_name': symptom.name,
        'symptom_id': symptom.id,
        'observed': symptom.observed,
        'details': symptom.details
    } for symptom in mapped_symptoms]


def get_admission_risk_factors(admission_id):
    observed_factors_ids = [obs.risk_factor_id for obs in Admission.query.get(admission_id).risk_factors]
    factors = [f for f in RiskFactor.query.all()]

    mapped_factors = []

    for factor in factors:
        if factor.id in observed_factors_ids:
            observed_factor = ObservedRiskFactor.query.filter_by(risk_factor_id=factor.id).first()
            factor.observed = observed_factor.observed
            factor.details = observed_factor.details
        else:
            factor.observed = None
            factor.details = ''
        mapped_factors.append(factor)
    return mapped_factors, [{
        'risk_factor_name': factor.name,
        'risk_factor_id': factor.id,
        'observed': factor.observed,
        'details': factor.details
    } for factor in mapped_factors]


def upsert_symptom(admission_id, obs_symptom_formdata):
    '''
    This method may create, update or remove an observed symptom
    from an admission.

    - Create: if there's no assigned observed symptom and the incoming
    hasn't been ignored.
    - Update: if there's already one assigned and has been updated to
    something else than ignored.
    - Delete: in the case there's already one assigned and it has been
    updated to ignored.
    '''
    obs_symptom_obj = ObservedSymptom.query.filter_by(
        admission_id=admission_id,
        symptom_id=obs_symptom_formdata['symptom_id'],
    ).first()

    if obs_symptom_formdata['observed'] is None:
        # Not assigned => don't do anything
        if obs_symptom_obj is None:
            return
        # Assigned => delete it
        db.session.delete(obs_symptom_obj)
        db.session.commit()
        return

    if obs_symptom_obj is None:
        obs_symptom_obj = ObservedSymptom()

    obs_symptom_obj.admission_id = admission_id
    obs_symptom_obj.symptom_id = obs_symptom_formdata['symptom_id']
    obs_symptom_obj.observed = obs_symptom_formdata['observed']
    obs_symptom_obj.details = obs_symptom_formdata['details']
    db.session.add(obs_symptom_obj)
    db.session.commit()


def upsert_risk_factor(admission_id, obs_factor_formdata):
    obs_factor_obj = ObservedRiskFactor.query.filter_by(
        admission_id=admission_id,
        risk_factor_id=obs_factor_formdata['risk_factor_id'],
    ).first()

    if obs_factor_formdata['observed'] is None:
        # Not assigned => don't do anything
        if obs_factor_obj is None:
            return
        # Assigned => delete it
        db.session.delete(obs_factor_obj)
        db.session.commit()
        return

    if obs_factor_obj is None:
        obs_factor_obj = ObservedRiskFactor()

    obs_factor_obj.admission_id = admission_id
    obs_factor_obj.risk_factor_id = obs_factor_formdata['risk_factor_id']
    obs_factor_obj.observed = obs_factor_formdata['observed']
    obs_factor_obj.details = obs_factor_formdata['details']
    db.session.add(obs_factor_obj)
    db.session.commit()


def get_dated_events(admission):
    mapped_dated_events = {}
    mapped_dated_events['vaccine'] = admission.vaccine
    mapped_dated_events['hospitalization'] = admission.hospitalization
    mapped_dated_events['uti_hospitalization'] = admission.utihospitalization
    mapped_dated_events['clinical_evolution'] = admission.clinicalevolution
    return mapped_dated_events


def upsert_dated_events(admission, dated_events_formdata):
    # Null dated events (so they are excluded)
    if admission.vaccine:
        admission.vaccine.admission = None
    if admission.hospitalization:
        admission.hospitalization.admission = None
    if admission.utihospitalization:
        admission.utihospitalization.admission = None
    if admission.clinicalevolution:
        admission.clinicalevolution.admission = None

    vaccine = Vaccine(admission=admission,
        **dated_events_formdata['vaccine'])
    hospitalization = Hospitalization(admission=admission,
        **dated_events_formdata['hospitalization'])
    uti_hospitalization = UTIHospitalization(admission=admission,
        **dated_events_formdata['uti_hospitalization'])
    clinical_evolution = ClinicalEvolution(admission=admission,
        **dated_events_formdata['clinical_evolution'])

    db.session.add(vaccine)
    db.session.add(hospitalization)
    db.session.add(uti_hospitalization)
    db.session.add(clinical_evolution)
    db.session.commit()


# TODO: merge antiviral and xray
def get_antiviral(admission):
    if admission.antiviral is None:
        admission.antiviral = Antiviral()
    return {
        'usage': admission.antiviral.usage,
        'other': admission.antiviral.other,
        'start_date': admission.antiviral.start_date,
    }


def upsert_antiviral(admission, antiviral_formdata):
    if admission.antiviral:
        admission.antiviral.admission = None
    antiviral = Antiviral(admission=admission, **{
        'usage': antiviral_formdata['usage'],
        'start_date': antiviral_formdata['start_date'],
        'other': antiviral_formdata['other'],
    })
    db.session.add(antiviral)
    db.session.commit()


def get_xray(admission):
    if admission.xray is None:
        admission.xray = XRay()
    return {
        'usage': admission.xray.usage,
        'other': admission.xray.other,
        'start_date': admission.xray.start_date,
    }


def upsert_xray(admission, xray_formdata):
    if admission.xray:
        admission.xray.admission = None
    xray = XRay(admission=admission, **{
        'usage': xray_formdata['usage'],
        'start_date': xray_formdata['start_date'],
        'other': xray_formdata['other'],
    })
    db.session.add(xray)
    db.session.commit()


def get_samples(admission):
    return admission.samples.order_by(Sample.id)


def add_sample(admission, form):
    sample = Sample(admission=admission)
    cdc_exam = CdcExam(sample=sample)
    form.cdc_exam.form.populate_obj(cdc_exam)
    form.populate_obj(sample)
    db.session.add(sample)
    db.session.commit()


def update_sample(sample, form):
    form.populate_obj(sample)
    db.session.add(sample)
    db.session.commit()
