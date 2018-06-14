import wtforms as wt

from . import models


def get_methods_choices():
    choices = [(m.id, m.name) for m in models.Method.query.all()]
    return choices


class MethodSelectField(wt.SelectField):
    def __init__(self, label='Método de Coleta', **kwargs):
        choices = get_methods_choices()
        super(MethodSelectField, self).__init__(
            label, choices=choices, coerce=int, **kwargs)
