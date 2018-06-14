create_countries_sql = "\
    INSERT INTO countries(id, name_en_us, name_pt_br, abbreviation) VALUES\
    (1, 'Brazil', 'Brasil', 'BR'),\
    (2, 'Argentina', 'Argentina', 'AR'),\
    \
    (9, 'Outro', 'Other', 'XX')\
    ON CONFLICT (id) DO NOTHING;"

create_regions_sql = "\
    INSERT INTO regions(id, country_id, name, region_code) VALUES\
    (1, 1, 'Norte', 1),\
    (2, 1, 'Nordeste', 2),\
    (3, 1, 'Sudeste', 3),\
    (4, 1, 'Sul', 4),\
    (5, 1, 'Centro-Oeste', 5)\
    ON CONFLICT (id) DO NOTHING;"

create_states_sql = "INSERT INTO states(id, region_id, name, uf_code) VALUES\
    (1, 1, 'Rio de Janeiro', 'RJ'),\
    (2, 1, 'Espírito Santo', 'ES'),\
    \
    (9, 1, 'Outro', 'XX')\
    ON CONFLICT (id) DO NOTHING;"

create_cities_sql = "INSERT INTO cities(id, state_id, name) VALUES\
    (1, 1, 'Rio de Janeiro'),\
    (2, 1, 'Niterói'),\
    \
    (9, 1, 'Outra')\
    ON CONFLICT (id) DO NOTHING;"

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
    \
    (12, 'Outro (especificar)', FALSE)\
    ON CONFLICT (id) DO NOTHING;"

create_stock = "INSERT INTO stocks(id, name) VALUES (1, 'Reativos')"


def load_data(db):
    db.engine.execute(create_methods)
    db.engine.execute(create_symptoms)
    db.engine.execute(create_stock)
