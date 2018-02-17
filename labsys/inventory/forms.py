import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, FieldList, FloatField, FormField,
                     HiddenField, IntegerField, Label, RadioField, SelectField,
                     StringField, SubmitField, ValidationError, widgets)
from wtforms.validators import InputRequired, DataRequired, Optional

from labsys.inventory.models import Product, StockProduct, Transaction


class AddTransactionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, ' {} | {}'.format(p.catalog, p.name))
                                   for p in Product.get_products()]

    product_id = SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    lot_number = StringField('Lote', validators=[InputRequired()])
    expiration_date = DateField(
        'Data de Validade', format='%d/%m/%Y', validators=[InputRequired()])
    amount = IntegerField('Quantidade Recebida', validators=[InputRequired()])
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
    details = StringField('Observações', validators=[Optional()])
    submit = SubmitField('Enviar')

    def validate_amount(self, field):
        stock_product = StockProduct.query.get(self.stock_product_id.data)
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
    name = StringField('Nome do Reativo', validators=[DataRequired()])
    manufacturer = StringField('Fabricante', validators=[DataRequired()])
    catalog = StringField('Número de Catálogo', validators=[DataRequired()])
    stock_unit = IntegerField(
        'Unidade de Estoque', default=1, validators=[DataRequired()])
    min_stock = IntegerField(
        'Estoque Mínimo (se produto unitário)',
        default=2,
        validators=[Optional()])
    subproduct_catalog = StringField(
        'Subproduto (Número de Catálogo)', validators=[Optional()])
    subproduct_id = HiddenField()
    submit = SubmitField('Cadastrar')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.stock_unit.data > 1:
            if self.subproduct_catalog.data == '' \
                    or self.subproduct_catalog.data is None:
                self.subproduct_catalog.errors.append(
                    'Subproduto deve ser preenchido para produtos '
                    'não unitários.')
                return False
        else:
            if self.subproduct_catalog.data != '' \
                    and self.subproduct_catalog.data is not None:
                self.subproduct_catalog.errors.append(
                    'Produtos unitários não possuem subproduto.')
                return False
        return True

    def validate_catalog(self, field):
        products_by_catalog_and_manufacturer = \
            Product.query.filter_by(
                catalog=field.data,
                manufacturer=self.manufacturer.data).all()
        if len(products_by_catalog_and_manufacturer) != 0:
            raise ValidationError(
                'Esse produto já está registrado no catálogo!')

    def validate_stock_unit(self, field):
        if field.data < 1:
            raise ValidationError(
                'Unidade de Estoque deve ser maior ou igual a 1.')

    def validate_min_stock(self, field):
        # Set min_stock = 0 for every non-unitary product
        if self.stock_unit.data != 1:
            field.data = 0

    def validate_subproduct_catalog(self, field):
        if field.data != '' and field.data is not None:
            manufacturer_products = Product.get_products_by_manufacturer(
                self.manufacturer.data)
            subproducts = [
                p.id for p in manufacturer_products if p.catalog == field.data
            ]
            if len(subproducts) == 0:
                raise ValidationError('Subproduto informado não existe.')
            elif Product.query.get(subproducts[0]).stock_unit != 1:
                raise ValidationError('Subproduto informado não é unitário.')
            else:
                self.subproduct_id.data = subproducts[0]
