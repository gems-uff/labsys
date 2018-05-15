from labsys.extensions import db
from labsys.admissions.models import ObservedSymptom, Admission, Symptom, RiskFactor, ObservedRiskFactor


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
