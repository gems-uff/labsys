import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, FormField, FormField, RadioField, HiddenField,
    FieldList, BooleanField, Label, DateField, SelectField, IntegerField,
    FloatField, widgets, ValidationError
)
from wtforms.validators import InputRequired, Optional
from ..models import Product


class AddTransactionForm(FlaskForm):
    catalog = SelectField('Número de Catálogo',
                                 validators=[InputRequired()])
    manufacturer = SelectField('fabricante', validators=[Optional()])
    reactive_id = SelectField('Produto', coerce=int,
                              validators=[InputRequired()])
    amount = IntegerField('Quantidade Recebida',
                          validators=[InputRequired()])
    transaction_date = DateField('Data de Registro',
                                    format='%d/%m/%Y',
                                    default=datetime.datetime.today(),
                                    validators=[InputRequired()])
    invoice = StringField('Nota Fiscal', validators=[Optional()])
    details = StringField('Observações', validators=[Optional()])
    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        if field.data < 1:
            raise ValidationError(
                'Quantidade de reativos deve ser maior ou igual a 1')


class SubTransactionForm(FlaskForm):
    catalog = StringField('Número do Catálogo', validators=[InputRequired()])
    reactive_id = SelectField('Produto', coerce=int,
                              validators=[InputRequired()])
    amount = IntegerField('Quantidade Consumida',
                          validators=[InputRequired()])
    transaction_date = DateField('Data de Uso',
                                    format='%d/%m/%Y',
                                    default=datetime.datetime.today(),
                                    validators=[InputRequired()])


    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        reactive = Reactive.query.get(form.reactive_id.data)
        if field.data < 1:
            raise ValidationError(
                'Quantidade de reativos deve ser maior ou igual a 1')
        elif (reactive.amount - field.data) < 0:
            raise ValidationError('Não há essa quantidade do reativo '
                                  'selecionado em estoque. O total é: {}'
                                  .format(reactive.amount))
        else:
            field.data = -field.data
