from labsys.extensions import db
from labsys.admissions.models import ObservedSymptom, Admission, Symptom


def get_admission_symptoms(admission_id):
    # query = 'SELECT s.id, s.name, s.primary, obs.observed, obs.details \
    #     FROM symptoms s \
    #     LEFT JOIN observed_symptoms obs \
    #         ON s.id = obs.symptom_id \
    #     WHERE obs.admission_id = %d OR obs.admission_id IS NULL' % admission_id
    # result = db.engine.execute(query)

    # mapped_symptoms = [{
    #     'entity_id': symptom[0],
    #     'entity_name': symptom[1],
    #     'primary': symptom[2],
    #     'observed': symptom[3],
    #     'details': symptom[4],
    # } for symptom in result.fetchall()]
    observed_symptoms_ids = [obs.symptom_id for obs in Admission.query.get(admission_id).symptoms]
    symptoms = [s for s in Symptom.query.all()]

    mapped_symptoms = []

    # import pdb; pdb.set_trace()
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
    query = 'SELECT rf.id, rf.name, rf.primary, obs.observed, obs.details \
        FROM risk_factors rf \
        LEFT JOIN observed_risk_factors obs \
            ON rf.id = obs.symptom_id \
        WHERE obs.admission_id = %d OR obs.admission_id IS NULL' % admission_id
    result = db.engine.execute(query)

    mapped_risk_factors = [
        {
            'entity_id': risk_factor[0],
            'entity_name': risk_factor[1],
            'primary': risk_factor[2],
            'observed': risk_factor[3],
            'details': risk_factor[4],
        } for risk_factor in result.fetchall()]
    return mapped_risk_factors

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