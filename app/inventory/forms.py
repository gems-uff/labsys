import datetime

from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, FormField, FormField,
                     RadioField, HiddenField, FieldList, BooleanField, Label,
                     DateField, SelectField, IntegerField, FloatField, widgets,
                     ValidationError)
from wtforms.validators import InputRequired, Optional
from ..models import Product, StockProduct, Transaction


class AddTransactionForm(FlaskForm):
    product_id = SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
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
    stock_product_id = SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    amount = IntegerField('Quantidade Consumida', validators=[InputRequired()])
    transaction_date = DateField(
        'Data de Uso',
        format='%d/%m/%Y',
        default=datetime.datetime.today(),
        validators=[InputRequired()])
    details = StringField('Observações', validators=[Optional()])
    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        stock_product = StockProduct.query.get(form.stock_product_id.data)
        if field.data < 1:
            raise ValidationError(
                'Quantidade Consumida deve ser maior ou igual a 1')
        elif (stock_product.amount < field.data):
            raise ValidationError(
                'Não há essa quantidade do reativo em estoque. O total é: {}'
                .format(stock_product.amount))
        else:
            field.data = -field.data


class ProductForm(FlaskForm):
    name = StringField('Nome do Reativo', validators=[InputRequired()])
    manufacturer = StringField('Fabricante', validators=[InputRequired()])
    catalog = StringField('Número de Catálogo', validators=[InputRequired()])
    stock_unit = IntegerField(
        'Unidade de Estoque', default=1, validators=[InputRequired()])
    subproduct_catalog = StringField(
        'Subproduto (Número de Catálogo)', validators=[Optional()])
    subproduct_id = HiddenField()
    submit = SubmitField('Cadastrar')

    def validate_subproduct_catalog(form, field):
        if field.data != '':
            manufacturer_products = Product.get_products_by_manufacturer(
                form.manufacturer.data)
            subproducts = [
                p.id for p in manufacturer_products if p.catalog == field.data
            ]
            if len(subproducts) == 0:
                raise ValidationError('Subproduto informado não existe.')
            else:
                form.subproduct_id.data = subproducts[0]
