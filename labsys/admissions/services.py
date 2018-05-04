from labsys.extensions import db


def get_admission_symptoms(admission_id):
    query = 'SELECT s.id, s.name, s.primary, obs.observed, obs.details \
        FROM symptoms s \
        LEFT JOIN observed_symptoms obs \
            ON s.id = obs.symptom_id \
        WHERE obs.admission_id = %d OR obs.admission_id IS NULL' % admission_id
    result = db.engine.execute(query)

    mapped_symptoms = [{
        'entity_id': symptom[0],
        'entity_name': symptom[1],
        'primary': symptom[2],
        'observed': symptom[3],
        'details': symptom[4],
    } for symptom in result.fetchall()]
    return mapped_symptoms


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
