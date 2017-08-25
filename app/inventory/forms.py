import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, FieldList, FloatField, FormField,
                     HiddenField, IntegerField, Label, RadioField, SelectField,
                     StringField, SubmitField, ValidationError, widgets)
from wtforms.validators import InputRequired, Optional

from ..models import Product, StockProduct, Transaction


class AddTransactionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, ' {} | {}'.format(p.catalog, p.name))
                                   for p in Product.get_products()]

    product_id = SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    lot_number = StringField('Lote', validators=[InputRequired()])
    expiration_date = DateField(
        'Data de Validade', format='%d/%m/%Y', validators=[Optional()])
    amount = IntegerField('Quantidade Recebida', validators=[InputRequired()])
    transaction_date = DateField(
        'Data de Registro',
        format='%d/%m/%Y',
        default=datetime.datetime.now(),
        validators=[InputRequired()])
    invoice_type = SelectField(
        'Tipo de Nota',
        coerce=str,
        choices=(('Nota Fiscal',
                  'Nota Fiscal'), ('Nota de Fornecimento (FIOCRUZ)',
                                   'Nota de Fornecimento (FIOCRUZ)'),
                 ('Nota de Fornecimento (Ministério da Saúde)',
                  'Nota de Fornecimento (Ministério da Saúde)'), ('Outros',
                                                                  'Outros')),
        default='Nota Fiscal',
        validators=[Optional()])
    invoice = StringField('Número da Nota', validators=[Optional()])
    financier = StringField('Projeto/Financiador', validators=[Optional()])
    details = StringField('Observações', validators=[Optional()])
    submit = SubmitField('Enviar')

    def validate_amount(form, field):
        if field.data < 1:
            raise ValidationError(
                'Quantidade Recebida deve ser maior ou igual a 1')


class SubTransactionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock_product_id.choices = [
            (sp.id, '{} | Lote: {} | Unidades: {} | {}'.format(
                sp.product.catalog, sp.lot_number, sp.amount, sp.product.name))
            for sp in StockProduct.list_products_in_stock()
        ]

    stock_product_id = SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    amount = IntegerField('Quantidade Consumida', validators=[InputRequired()])
    transaction_date = DateField(
        'Data de Uso',
        format='%d/%m/%Y',
        default=datetime.datetime.now(),
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
    min_stock = IntegerField(
        'Estoque Mínimo (se produto unitário)',
        default=2,
        validators=[Optional()])
    subproduct_catalog = StringField(
        'Subproduto (Número de Catálogo)', validators=[Optional()])
    subproduct_id = HiddenField()
    submit = SubmitField('Cadastrar')

    def validate_stock_unit(form, field):
        if field.data < 1:
            raise ValidationError(
                'Unidade de Estoque deve ser maior ou igual a 1.')

    def validate_min_stock(form, field):
        # Set min_stock = 0 for every non-unitary product
        if form.stock_unit.data != 1:
            field.data = 0

    def validate_subproduct_catalog(form, field):
        '''
        TODO: make this validation be called even though field is empty
        if form.stock_unit.data > 1 and field.data == '':
            raise ValidationError(
                'Catálogo de subproduto deve ser informado para produtos não unitários.'
            )
        '''
        if field.data != '':
            manufacturer_products = Product.get_products_by_manufacturer(
                form.manufacturer.data)
            subproducts = [
                p.id for p in manufacturer_products if p.catalog == field.data
            ]
            if len(subproducts) == 0:
                raise ValidationError('Subproduto informado não existe.')
            elif Product.query.get(subproducts[0]).stock_unit != 1:
                raise ValidationError('Subproduto informado não é unitário.')
            else:
                form.subproduct_id.data = subproducts[0]
