import datetime

from flask import (
    render_template, session, redirect, url_for, current_app, flash, request,
    abort,
)
from flask_login import current_user

from app import inventory
from .. import db
from ..models import (
    Transaction, Reactive
)
from . import inventory
from .forms import AddTransactionForm


@inventory.route('/', methods=['GET'])
def index():
    return render_template('inventory/index.html')


@inventory.route('/reactives', methods=['GET'])
def list_reactives():
    return render_template('inventory/list-reactives.html')


@inventory.route('/transactions', methods=['GET'])
def list_transactions():
    return render_template('inventory/list-transactions.html')


@inventory.route('/transactions/add-reactive', methods=['GET', 'POST'])
def add_reactive():
    form = AddTransactionForm()
    form.reactive_id.choices = [
        (r.id, r.name) for r in Reactive.get_reactives()]
    if form.validate_on_submit():
        transaction = Transaction(
            transaction_date=form.transaction_date.data,
            amount=form.amount.data,
            reactive_id=form.reactive_id.data,
            user=current_user
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Reativo adicionado com sucesso.')
        return redirect(url_for('.add_reactive'))

    return render_template(
        'inventory/add-reactive.html', form=form)


@inventory.route('/transactions/subtract-reactive')
def subtract_reactive():
    return 'Not implemented yet'
