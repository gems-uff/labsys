import datetime

from flask import (
    render_template, session, redirect, url_for, current_app, flash, request,
    abort,
)
from flask_login import current_user

from app import inventory
from .. import db
from ..models import (
    Transaction, Product
)
from . import inventory
from .forms import AddTransactionForm, SubTransactionForm


@inventory.route('/', methods=['GET'])
def index():
    return render_template('inventory/index.html')


@inventory.route('/products', methods=['GET'])
def list_products():
    return render_template('inventory/list-products.html')


@inventory.route('/transactions', methods=['GET'])
def list_transactions():
    return render_template('inventory/list-transactions.html')


@inventory.route('/transactions/<string:method>', methods=['GET', 'POST'])
def create_transaction(method):
    form = AddTransactionForm() if method == 'add' else SubTransactionForm()
    form.product_id.choices = [
        (p.id, p.name) for p in Product.get_products()]
    if form.validate_on_submit():
        transaction = Transaction(
            transaction_date=form.transaction_date.data,
            amount=form.amount.data,
            product_id=form.product_id.data,
            invoice=form.invoice.data,
            details=form.details.data,
            user=current_user
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transação cadastrada com sucesso.')
        return redirect(url_for('.create_transaction', method=method))

    return render_template(
        'inventory/create-transaction.html', form=form, method=method)
