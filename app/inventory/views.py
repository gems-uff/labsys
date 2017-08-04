import datetime

from flask import (
    render_template,
    session,
    redirect,
    url_for,
    current_app,
    flash,
    request,
    abort, )
from flask_login import current_user

from app import inventory
from .. import db
from ..models import (Transaction, Product)
from . import inventory
from .forms import AddTransactionForm, SubTransactionForm


@inventory.route('/', methods=['GET'])
def index():
    return render_template('inventory/index.html')


@inventory.route('/products', methods=['GET'])
def list_products():
    return render_template('inventory/list-products.html')


@inventory.route('/products/add', methods=['GET', 'POST'])
def create_product():
    return 'Not implemented yet'


@inventory.route('/transactions', methods=['GET'])
def list_transactions():
    return render_template('inventory/list-transactions.html')


@inventory.route('/transactions/add', methods=['GET', 'POST'])
def create_add_transaction():
    form = AddTransactionForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.get_products()]
    if form.validate_on_submit():
        transaction = Transaction(
            product_allotment=form.allotment.data,
            product_id=form.product_id.data,
            amount=form.amount.data,
            invoice=form.invoice.data,
            transaction_date=form.transaction_date.data,
            details=form.details.data,
            user=current_user)
        db.session.add(transaction)
        db.session.commit()
        flash('Entrada realizada com sucesso.')
        return redirect(url_for('.create_add_transaction', method='add'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='add')


@inventory.route('/transactions/sub', methods=['GET', 'POST'])
def create_sub_transaction():
    form = SubTransactionForm()
    form.product_id.choices = [(
        p.id, p.name) for p in Product.get_products(unitary_only=True)]
    if form.validate_on_submit():
        transaction = Transaction(
            product_id=form.product_id.data,
            allotment=form.allotment.data,
            amount=form.amount.data,
            transaction_date=form.transaction_date.data,
            details=form.details.data,
            user=current_user)
        db.session.add(transaction)
        db.session.commit()
        flash('Baixa realizada com sucesso.')
        return redirect(url_for('.create_sub_transaction', method='sub'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='sub')
