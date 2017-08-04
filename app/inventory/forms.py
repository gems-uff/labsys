import datetime

from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, FormField, FormField,
                     RadioField, HiddenField, FieldList, BooleanField, Label,
                     DateField, SelectField, IntegerField, FloatField, widgets,
                     ValidationError)
from wtforms.validators import InputRequired, Optional
from ..models import Product, Transaction


class AddTransactionForm(FlaskForm):
    # fabricante, catalogo
    product_id = SelectField(
        'Produto', coerce=int, validators=[InputRequired()])
    allotment = StringField('Lote', validators=[InputRequired()])
    amount = IntegerField('Quantidade Recebida', validators=[InputRequired()])
    transaction_date = DateField(
        'Data de Registro',
        format='%d/%m/%Y',
        default=datetime.datetime.today(),
        validators=[InputRequired()])
    invoice = StringField('Nota Fiscal', validators=[Optional()])
    details = StringField('Observações', validators=[Optional()])
    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        if field.data < 1:
            raise ValidationError(
                'Quantidade Recebida deve ser maior ou igual a 1')


class SubTransactionForm(FlaskForm):
    product_id = SelectField(
        'Produto', coerce=int, validators=[InputRequired()])
    allotment = StringField('Lote', validators=[InputRequired()])
    amount = IntegerField('Quantidade Consumida', validators=[InputRequired()])
    transaction_date = DateField(
        'Data de Uso',
        format='%d/%m/%Y',
        default=datetime.datetime.today(),
        validators=[InputRequired()])
    details = StringField('Observações', validators=[Optional()])
    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        product = (form.product_id.data, form.allotment.data)
        if field.data < 1:
            raise ValidationError(
                'Quantidade Consumida deve ser maior ou igual a 1')
        elif (Transaction.get_product_amount(product) < field.data):
            raise ValidationError(
                'Não há essa quantidade do produto em estoque. O total é: {}'
                .format(product[0]))
        else:
            field.data = -field.data
