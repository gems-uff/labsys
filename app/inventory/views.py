from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app.inventory.utils import stock_is_at_minimum
from app.decorators import permission_required
from app.email import send_email
from .. import db
from ..models import (Transaction, Product, StockProduct, Permission, User)
from . import inventory
from .forms import AddTransactionForm, SubTransactionForm, ProductForm


@inventory.route('/', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def index():
    products = Product.get_products(unitary_only=True)
    for p in products:
        p.aggregate_amount = p.count_amount_stock_products()
        print(p.aggregate_amount)
    return render_template('inventory/index.html', products=products)


@inventory.route('/catalog', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def list_catalog():
    catalog = Product.get_products()
    return render_template('inventory/list-catalog.html', catalog=catalog)


@inventory.route('/reactives/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def create_reactive():
    form = ProductForm()
    if form.validate_on_submit():
        reactive = Product()
        form.populate_obj(reactive)
        if form.subproduct_id.data != '':
            reactive.subproduct = Product.query.get(form.subproduct_id.data)
        db.session.add(reactive)
        db.session.commit()
        flash('Reativo cadastrado com sucesso!')
        return redirect(url_for('.create_reactive'))
    return render_template('inventory/create-reactive.html', form=form)


@inventory.route('/transactions', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def list_transactions():
    transactions = Transaction.get_transactions_ordered()
    return render_template(
        'inventory/list-transactions.html', transactions=transactions)


@inventory.route('/transactions/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def create_add_transaction():
    form = AddTransactionForm()
    form.product_id.choices = [(p.id, ' ({}) {}'.format(p.catalog, p.name))
                               for p in Product.get_products()]
    if form.validate_on_submit():
        transaction = Transaction(user=current_user)
        form.populate_obj(transaction)
        catalog_product = Product.query.get(transaction.product_id)
        # Unitary product
        if catalog_product.is_unitary:
            transaction.stock_product = StockProduct.query.filter_by(
                product_id=catalog_product.id,
                lot_number=form.lot_number.data).first()
            if transaction.stock_product is None:
                transaction.stock_product = StockProduct(
                    product_id=catalog_product.id,
                    lot_number=form.lot_number.data,
                    expiration_date=form.expiration_date.data,
                    amount=transaction.amount, )
            else:
                transaction.stock_product.amount += transaction.amount
        # Non-Unitary => convert parent to child
        else:
            product_id = catalog_product.subproduct.id
            transaction.stock_product = StockProduct.query.filter_by(
                product_id=product_id,
                lot_number=form.lot_number.data).first()
            if transaction.stock_product is None:
                transaction.stock_product = StockProduct(
                    product_id=product_id,
                    lot_number=form.lot_number.data,
                    expiration_date=form.expiration_date.data,
                    amount=(transaction.amount * catalog_product.stock_unit))
            else:
                transaction.stock_product.amount += (
                    transaction.amount * catalog_product.stock_unit)
        db.session.add(transaction)
        db.session.commit()
        flash('Entrada realizada com sucesso.')
        return redirect(url_for('.create_add_transaction', method='add'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='add')


@inventory.route('/transactions/sub', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def create_sub_transaction():
    form = SubTransactionForm()
    form.stock_product_id.choices = [
        (sp.id, sp.product.name + ' | Lote: ' + sp.lot_number +
         ' | {} unidades.'.format(sp.amount))
        for sp in StockProduct.list_products_in_stock()
    ]
    if form.validate_on_submit():
        lot_number = StockProduct.query.get(
            form.stock_product_id.data).lot_number
        transaction = Transaction(user=current_user)
        form.populate_obj(transaction)
        transaction.stock_product = StockProduct.query.get(
            transaction.stock_product_id)
        # transaction.amount is negative (form changes its sign)
        transaction.stock_product.amount += transaction.amount
        transaction.product = transaction.stock_product.product
        if stock_is_at_minimum(transaction.stock_product, transaction.product):
            send_email(
                User.get_stock_alert_emails(),
                'Alerta de Estoque',
                'inventory/email/stock_alert',
                reactive_name=transaction.product.name,
                amount_in_stock=
                transaction.product.count_amount_stock_products(),
                min_stock=transaction.stock_product.product.min_stock)
        db.session.add(transaction)
        db.session.commit()
        flash('Baixa realizada com sucesso.')
        return redirect(url_for('.create_sub_transaction', method='sub'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='sub')
