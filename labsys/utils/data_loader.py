create_methods = "INSERT INTO methods(id, name, \"primary\") VALUES\
    (1, 'Swab Triplo', TRUE),\
    (2, 'Secreção de oro e nasofaringe', TRUE),\
    (3, 'Tecido post-mortem', TRUE),\
    (4, 'Lavado Bronco-alveolar', TRUE),\
    (5, 'Outro, especifique', TRUE)\
    ON CONFLICT (id) DO NOTHING;"

create_symptoms = "INSERT INTO symptoms(id, name, \"primary\") VALUES\
    (1, 'Febre', TRUE),\
    (2, 'Tosse', TRUE),\
    (3, 'Dor de garganta', TRUE),\
    (4, 'Dispneia', TRUE),\
    (5, 'Mialgia', TRUE),\
    (6, 'Saturação de O₂ < 95%%', TRUE),\
    (7, 'Desconforto respiratório', TRUE),\
    (8, 'Outros sinais e sintomas', TRUE),\
    (9, 'Dor de cabeça', FALSE),\
    (10, 'Azia', FALSE),\
    (11, 'Desmaios', FALSE),\
    (12, 'Outro (especificar)', FALSE)\
    ON CONFLICT (id) DO NOTHING;"

create_stock = "INSERT INTO stocks(id, name) VALUES (1, 'Reativos')"


def load_data(db):
    db.engine.execute(create_methods)
    db.engine.execute(create_symptoms)
    db.engine.execute(create_stock)
