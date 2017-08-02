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


@inventory.route('/reactives', methods=['GET'])
def list_reactives():
    return render_template('inventory/list-reactives.html')


@inventory.route('/transactions', methods=['GET'])
def list_transactions():
    return render_template('inventory/list-transactions.html')


@inventory.route('/transactions/<string:method>', methods=['GET', 'POST'])
def create_transaction(method):
    form = AddTransactionForm() if method == 'add' else SubTransactionForm()
    form.reactive_id.choices = [
        (r.id, r.name) for r in Reactive.get_reactives()]
    if form.validate_on_submit():
        transaction = Transaction(
            transaction_date=form.transaction_date.data,
            amount=form.amount.data,
            reactive_id=form.reactive_id.data,
            catalog_number=form.catalog_number.data,
            manufacturer=form.manufacturer.data,
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
