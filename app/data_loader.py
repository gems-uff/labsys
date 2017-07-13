from app.models import Country, Region, State, City, Method, Symptom


create_countries_sql = "\
INSERT INTO countries(id, name_en_us, name_pt_br, abbreviation) VALUES\
    (1, 'Brazil', 'Brasil', 'BR');\
"

create_regions_sql = "\
INSERT INTO regions(id, country_id, name, region_code) VALUES\
    (1, 1, 'Norte', 1),\
    (2, 1, 'Nordeste', 2),\
    (3, 1, 'Sudeste', 3),\
    (4, 1, 'Sul', 4),\
    (5, 1, 'Centro-Oeste', 5);\
"

create_states_sql = "\
INSERT INTO states(id, region_id, name, uf_code) VALUES\
    (1, 1, 'Rio de Janeiro', 'RJ');\
"


create_cities_sql = "\
INSERT INTO cities(id, state_id, name) VALUES\
    (1, 1, 'Rio de Janeiro'),\
    (2, 1, 'Niterói');\
"


def load_data(db):
    db.engine.execute(create_countries_sql)
    db.engine.execute(create_regions_sql)
    db.engine.execute(create_states_sql)
    db.engine.execute(create_cities_sql)
