import datetime as dt

import wtforms as wtf
import wtforms.widgets.html5 as widgets
from flask_wtf import FlaskForm
from wtforms.validators import (DataRequired, InputRequired, NumberRange,
                                Optional)

import labsys.inventory.models as models
from labsys.inventory.models import Product, StockProduct, Transaction


class OrderItemForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        specs = kwargs.get('specs', [])
        self.item_id.choices = [
            (s.id, '{} | Catálogo: {} | {} unidades/produto'.format(
                s.product.name, s.catalog_number, s.units))
            for s in specs]

    # TODO: make my own select field for foreign keys
    item_id = wtf.SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    amount = wtf.IntegerField(
        'Quantidade',
        widget=widgets.NumberInput(),
        render_kw={"autocomplete": "off"},
        validators=[
            InputRequired(),
            NumberRange(
                min=1, max=None, message='Quantidade deve ser maior que zero!')
        ])
    lot_number = wtf.StringField(
        'Lote', render_kw={"autocomplete": "off"}, validators=[InputRequired()]
    )
    expiration_date = wtf.DateField(
        'Data de Validade',
        widget=widgets.DateInput(),
        validators=[InputRequired()])
    add_product = wtf.SubmitField('Adicionar produto ao carrinho')
    finish_order = wtf.SubmitField('Ir para checkout')
    cancel = wtf.SubmitField('Limpar o carrinho')


class OrderForm(FlaskForm):
    invoice_type = wtf.SelectField(
        'Tipo de Nota',
        coerce=str,
        choices=(
            ('Nota Fiscal',
             'Nota Fiscal'),
            ('Nota de Fornecimento (FIOCRUZ)',
             'Nota de Fornecimento (FIOCRUZ)'),
            ('Nota de Fornecimento (Ministério da Saúde)',
             'Nota de Fornecimento (Ministério da Saúde)'),
            ('Outros', 'Outros')),
        default='Nota Fiscal',
        validators=[Optional()])
    invoice = wtf.StringField('Nota', validators=[Optional()])
    financier = wtf.StringField('Financiador', validators=[Optional()])
    notes = wtf.StringField('Observações', validators=[Optional()])
    submit = wtf.SubmitField('Finalizar a compra', render_kw={'class': 'btn-danger'})
    cancel = wtf.SubmitField('Limpar o carrinho')


class ConsumeProductForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stock_products = kwargs.get('stock_products', [])
        self.stock_product_id.choices = [
            (sp.id, 'Nome: {} | Catálogo: {} | Lote: {} | Quantidade: {}'
                .format(
                    sp.product.name,
                    sp.product.get_base_spec().catalog_number,
                    sp.lot_number,
                    sp.amount,
                ))
            for sp in stock_products]

    stock_product_id = wtf.SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    amount = wtf.IntegerField('Quantidade', validators=[
        InputRequired(),
        NumberRange(
            min=1, max=None, message='Quantidade deve ser maior que zero!')],
        widget=widgets.NumberInput(),
        render_kw={'autocomplete': 'off'},
        default=1,
    )
    submit = wtf.SubmitField('Confirmar')


class AddProductForm(FlaskForm):
    name = wtf.StringField(
        'Nome do reativo', validators=[InputRequired()])
    stock_minimum = wtf.IntegerField(
        'Estoque mínimo', default=1, validators=[
            InputRequired(),
            NumberRange(
                min=1, max=None, message='Deve ser maior que zero!')],
        widget=widgets.NumberInput(),
        render_kw={'autocomplete': 'off'},
    )
    manufacturer = wtf.StringField(
        'Fabricante', validators=[InputRequired()])
    catalog_number = wtf.StringField(
        'Número de catálogo', validators=[InputRequired()])
    units = wtf.IntegerField(
        'Unidades de estoque', default=1, validators=[
            InputRequired(),
            NumberRange(
                min=1, max=None, message='Deve ser maior que zero!')],
        widget=widgets.NumberInput(),
        render_kw={'autocomplete': 'off'},
    )
    submit = wtf.SubmitField('Cadastrar Reativo')

    def validate_spec_catalog(self, field):
        spec = models.Specification.query.filter_by(
            catalog_number=field.data,
            manufacturer=self.manufacturer.data).first()
        if spec is not None:
            raise wtf.ValidationError(
                'Essa especificação já está cadastrada (catálogo e fabricante')


class AddSpecificationForm(FlaskForm):
    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.data = product_id

    product_id = wtf.HiddenField()
    manufacturer = wtf.StringField('Fabricante', validators=[InputRequired()])
    catalog_number = wtf.StringField('Catálogo', validators=[InputRequired()])
    units = wtf.IntegerField(
        'Unidades de estoque', default=1, validators=[
            InputRequired(),
            NumberRange(
                min=1, max=None, message='Deve ser maior que zero!')],
        widget=widgets.NumberInput(),
        render_kw={'autocomplete': 'off'},
    )
    submit = wtf.SubmitField('Confirmar')


# DEPRECATED

class AddTransactionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, ' {} | {}'.format(p.catalog, p.name))
                                   for p in Product.get_products()]

    product_id = wtf.SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    lot_number = wtf.StringField('Lote', validators=[InputRequired()])
    expiration_date = wtf.DateField(
        'Data de Validade', format='%d/%m/%Y', validators=[InputRequired()])
    amount = wtf.IntegerField('Quantidade Recebida', validators=[
        InputRequired(),
        NumberRange(
            min=1, max=None, message='Quantidade deve ser maior que zero!')])
    invoice_type = wtf.SelectField(
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
    invoice = wtf.StringField('Número da Nota', validators=[Optional()])
    financier = wtf.StringField('Projeto/Financiador', validators=[Optional()])
    details = wtf.StringField('Observações', validators=[Optional()])
    submit = wtf.SubmitField('Enviar')

    def validate_amount(self, field):
        if field.data < 1:
            raise wtf.ValidationError(
                'Quantidade Recebida deve ser maior ou igual a 1')


class SubTransactionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock_product_id.choices = [
            (sp.id, '{} | Lote: {} | Unidades: {} | {}'.format(
                sp.product.catalog, sp.lot_number, sp.amount, sp.product.name))
            for sp in StockProduct.list_products_in_stock()
        ]

    stock_product_id = wtf.SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    amount = wtf.IntegerField('Quantidade Consumida', validators=[
        InputRequired(),
        NumberRange(
            min=1, max=None, message='Quantidade deve ser maior que zero!')])

    details = wtf.StringField('Observações', validators=[Optional()])
    submit = wtf.SubmitField('Enviar')

    def validate_amount(self, field):
        stock_product = StockProduct.query.get(self.stock_product_id.data)
        if field.data < 1:
            raise wtf.ValidationError(
                'Quantidade Consumida deve ser maior ou igual a 1')
        elif (stock_product.amount < field.data):
            raise wtf.ValidationError(
                'Não há essa quantidade do reativo em estoque. O total é: {}'
                .format(stock_product.amount))
        else:
            field.data = -field.data


class ProductForm(FlaskForm):
    name = wtf.StringField('Nome do Reativo', validators=[DataRequired()])
    manufacturer = wtf.StringField('Fabricante', validators=[DataRequired()])
    catalog = wtf.StringField('Número de Catálogo', validators=[DataRequired()])
    stock_unit = wtf.IntegerField(
        'Unidade de Estoque', default=1, validators=[DataRequired()])
    min_stock = wtf.IntegerField(
        'Estoque Mínimo (se produto unitário)',
        default=2,
        validators=[Optional()])
    subproduct_catalog = wtf.StringField(
        'Subproduto (Número de Catálogo)', validators=[Optional()])
    subproduct_id = wtf.HiddenField()
    submit = wtf.SubmitField('Cadastrar')

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
            raise wtf.ValidationError(
                'Esse produto já está registrado no catálogo!')

    def validate_stock_unit(self, field):
        if field.data < 1:
            raise wtf.ValidationError(
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
                raise wtf.ValidationError('Subproduto informado não existe.')
            elif Product.query.get(subproducts[0]).stock_unit != 1:
                raise wtf.ValidationError('Subproduto informado não é unitário.')
            else:
                self.subproduct_id.data = subproducts[0]
