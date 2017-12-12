import datetime as dt

from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import InputRequired, DataRequired, Optional

from labsys.inventory.models import Product, StockProduct, Transaction


class OrderItemForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = kwargs.get('products', [])
        specs = kwargs.get('specs', [])
        self.product_id.choices = [(p.id, p.name) for p in products]
        self.item_id.choices = [
            (s.id, '{}x | Cat: {}'.format(s.units, s.catalog_number))
            for s in specs]

    # TODO: make my own select field for foreign keys
    product_id = wtf.SelectField(
        'Reativo', coerce=int, validators=[InputRequired()])
    item_id = wtf.SelectField(
        'Especificação', coerce=int, validators=[InputRequired()])
    amount = wtf.IntegerField('Quantidade', validators=[InputRequired()])
    lot_number = wtf.StringField('Lote', validators=[InputRequired()])
    expiration_date = wtf.DateField('Data de Validade',
                                    format='%d/%m/%Y',
                                    validators=[InputRequired()])
    add_product = wtf.SubmitField('Adicionar produto')
    finish_order = wtf.SubmitField('Finalizar compra')


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
    submit = wtf.SubmitField('Finalizar')
    cancel = wtf.SubmitField('Cancelar')


class ConsumeProductForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = kwargs.get('products', [])
        stock_products = kwargs.get('stock_products', [])
        lot_numbers = kwargs.get('lot_numbers', [])
        self.product_id.choices = [(p.id, p.name) for p in products]
        self.lot_number.choices = [
            (sp.id, 'Número: {} | Validade: {} | Quantidade: {}'.format(
                sp.lot_number, sp.expiration_date, sp.amount))
            for sp in stock_products]

    product_id = wtf.SelectField(
        'Produto', coerce=int, validators=[InputRequired()])
    lot_number = wtf.SelectField(
        'Lote', coerce=int, validators=[InputRequired()])
    amount = wtf.IntegerField('Quantidade', validators=[InputRequired()])
    submit = wtf.SubmitField('Confirmar')


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
    amount = wtf.IntegerField('Quantidade Recebida', validators=[InputRequired()])
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

    def validate_amount(form, field):
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
    amount = wtf.IntegerField('Quantidade Consumida', validators=[InputRequired()])
    details = wtf.StringField('Observações', validators=[Optional()])
    submit = wtf.SubmitField('Enviar')

    def validate_amount(form, field):
        stock_product = StockProduct.query.get(form.stock_product_id.data)
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

    def validate_catalog(form, field):
        products_by_catalog_and_manufacturer = \
            Product.query.filter_by(
                catalog = field.data,
                manufacturer = form.manufacturer.data).all()
        if len(products_by_catalog_and_manufacturer) != 0:
            raise wtf.ValidationError(
                'Esse produto já está registrado no catálogo!')

    def validate_stock_unit(form, field):
        if field.data < 1:
            raise wtf.ValidationError(
                'Unidade de Estoque deve ser maior ou igual a 1.')

    def validate_min_stock(form, field):
        # Set min_stock = 0 for every non-unitary product
        if form.stock_unit.data != 1:
            field.data = 0

    def validate_subproduct_catalog(form, field):
        if field.data != '' and field.data is not None:
            manufacturer_products = Product.get_products_by_manufacturer(
                form.manufacturer.data)
            subproducts = [
                p.id for p in manufacturer_products if p.catalog == field.data
            ]
            if len(subproducts) == 0:
                raise wtf.ValidationError('Subproduto informado não existe.')
            elif Product.query.get(subproducts[0]).stock_unit != 1:
                raise wtf.ValidationError('Subproduto informado não é unitário.')
            else:
                form.subproduct_id.data = subproducts[0]
