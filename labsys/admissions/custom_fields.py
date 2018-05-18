import wtforms as wt
from . import models


def get_methods_choices():
    choices = [(-1, '--------')]
    choices += [(m.id, m.name) for m in models.Method.query.all()]
    return choices


class MethodSelectField(wt.SelectField):
    def __init__(self, label='Método de Coleta', **kwargs):
        choices = get_methods_choices()
        super(MethodSelectField, self).__init__(
            label, default=-1, choices=choices, coerce=int, **kwargs)
