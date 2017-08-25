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
    if form.validate_on_submit():
        transaction = Transaction(user=current_user)
        form.populate_obj(transaction)
        transaction.receive_product(form.lot_number.data,
                                    form.expiration_date.data)
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
    if form.validate_on_submit():
        transaction = Transaction(user=current_user)
        form.populate_obj(transaction)
        transaction.consume_product()
        db.session.add(transaction)
        db.session.commit()
        flash('Baixa realizada com sucesso.')
        if stock_is_at_minimum(transaction.stock_product.product):
            send_email(
                User.get_stock_alert_emails(),
                'Alerta de Estoque',
                'inventory/email/stock_alert',
                reactive_name=transaction.stock_product.product.name,
                amount_in_stock=transaction.stock_product.product.
                count_amount_stock_products(),
                min_stock=transaction.stock_product.product.min_stock)
        return redirect(url_for('.create_sub_transaction', method='sub'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='sub')


@inventory.route('/transactions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def edit_add_transaction(id):
    #transaction = Transaction.query.get_or_404(id)
    form = AddTransactionForm()

    return render_template(
        'inventory/create-transaction.html', form=form, method='add')
