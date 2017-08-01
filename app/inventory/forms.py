import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, FormField, FormField, RadioField, HiddenField,
    FieldList, BooleanField, Label, DateField, SelectField, IntegerField,
    FloatField, widgets, ValidationError
)
from wtforms.validators import InputRequired, Optional
from ..models import Reactive


class AddTransactionForm(FlaskForm):
    reactive_id = SelectField('Reativo', coerce=int,
                              validators=[InputRequired()])
    amount = IntegerField('Quantidade',
                          validators=[InputRequired()])
    transaction_date = DateField('Data do Registro',
                                    format='%d/%m/%Y',
                                    default=datetime.datetime.today(),
                                    validators=[InputRequired()])
    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        reactive = Reactive.query.get(form.reactive_id.data)
        if (reactive.amount + field.data) < 0:
            raise ValidationError('Não há essa quantidade do reativo '
                                  'selecionado em estoque. O máximo é: {}'
                                  .format(reactive.amount))


