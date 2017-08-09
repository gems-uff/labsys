import wtforms as wt
import labsys.models as models


def get_cities_choices():
    choices = [(-1, '--------')]
    choices += [(c.id, c.name) for c in models.City.query.all()]
    return choices

def get_states_choices():
    choices = [(-1, '--------')]
    choices += [(s.id, s.uf_code) for s in models.State.query.all()]
    return choices

def get_countries_choices():
    choices = [(-1, '--------')]
    choices += [(c.id, c.name_pt_br) for c in models.Country.query.all()]
    return choices

def get_methods_choices():
    choices = [(-1, '--------')]
    choices += [(m.id, m.name) for m in models.Method.query.all()]
    return choices


class CitySelectField(wt.SelectField):
    def __init__(self, label='Cidade', **kwargs):
        choices = get_cities_choices()
        super(CitySelectField, self).__init__(
            label, default=-1, choices=choices, coerce=int, **kwargs)


class StateSelectField(wt.SelectField):
    def __init__(self, label='Estado (UF)', **kwargs):
        choices = get_states_choices()
        super(StateSelectField, self).__init__(
            label, default=-1, choices=choices, coerce=int, **kwargs)


class CountrySelectField(wt.SelectField):
    def __init__(self, label='País', **kwargs):
        choices = get_countries_choices()
        super(CountrySelectField, self).__init__(
            label, default=-1, choices=choices, coerce=int, **kwargs)


class MethodSelectField(wt.SelectField):
    def __init__(self, label='Método de Coleta', **kwargs):
        choices = get_methods_choices()
        super(MethodSelectField, self).__init__(
            label, default=-1, choices=choices, coerce=int, **kwargs)
