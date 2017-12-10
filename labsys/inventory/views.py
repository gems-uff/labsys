import logging

from flask import (
    render_template, redirect, url_for, flash, abort, Blueprint, session,
    request,
)
from flask_login import current_user, login_required

from ..extensions import db
from ..auth.decorators import permission_required
from ..auth.models import Permission, User
from ..utils.email import send_email
from .forms import AddTransactionForm, SubTransactionForm, ProductForm
from .utils import stock_is_at_minimum, export_table
from .models import (
    Transaction, Product, Stock, StockProduct, Specification, OrderItem,
)

import labsys.inventory.forms as forms

blueprint = Blueprint('inventory', __name__)

@blueprint.route('/', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def index():
    return render_template('inventory/index.html')


@blueprint.route('/products', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def list_catalog():
    products = Product.query.all()
    return render_template('inventory/list-products.html', products=products)


@blueprint.route('/orders/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def create_order():
    logging.info('create_order()')
    products = Product.query.all()
    specifications = Specification.query.all()
    form_context = {
        'products': products,
        'specs': specifications,
    }
    form = forms.OrderForm(**form_context)
    if session.get('order_items') is None:
        session['order_items'] = []

    if request.method == 'POST':
        logging.info('POSTing to create_order')
        if form.finish_order.data is True:
            logging.info('checking if there is at least 1 o_item in session')
            if len(session.get('order_items')) > 0:
                logging.info('Finishing order => redirect to checkout()')
                return redirect(url_for('inventory.checkout'))
            logging.info('None order item added to session')
            flash('Pelo menos 1 produto deve ser adicionado ao carrinho.')
            return render_template('inventory/create-order.html', form=form)
        if form.validate():
            logging.info('Create order form is valid')
            order_item = OrderItem()
            form.populate_obj(order_item)
            logging.info('order_item obj was populated')
            if len(session.get('order_items')) is 0:
                logging.info('order_items not found in session => create [oi]')
                session['order_items'] = [order_item.toJSON()]
            else:
                logging.info('order_items found in session => append(oi)')
                session['order_items'].append(order_item.toJSON())
                # See http://flask.pocoo.org/docs/0.12/api/#sessions
                # Must be manually set
                session.modified = True

            logging.info('finishing form.validate')
        logging.info('returning render template with or w/out errors and form')
        return render_template('inventory/create-order.html', form=form)
    logging.info('GETting create_order')
    return render_template('inventory/create-order.html', form=form)


@blueprint.route('/orders/checkout', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def checkout():
    session['order_items'] = []
    return 'Checkout pages'


@blueprint.route('/reactives/add', methods=['GET', 'POST'])
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


@blueprint.route('/transactions', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def list_transactions():
    transactions = Transaction.get_transactions_ordered()
    return render_template(
        'inventory/list-transactions.html', transactions=transactions)


@blueprint.route('/transactions/add', methods=['GET', 'POST'])
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


@blueprint.route('/transactions/sub', methods=['GET', 'POST'])
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


@blueprint.route('/transactions/add/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
# TODO: only owner or admin can edit a transaction
# TODO: can only edit add transactions
def edit_add_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = AddTransactionForm(
        obj=transaction,
        lot_number=transaction.stock_product.lot_number,
        expiration_date=transaction.stock_product.expiration_date)
    if form.validate_on_submit():
        Transaction.revert(transaction)
        # Normal add flow
        form.populate_obj(transaction)
        transaction.receive_product(form.lot_number.data,
                                    form.expiration_date.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Entrada atualizada com sucesso.')
        return redirect(url_for('.edit_add_transaction', id=id, method='add'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='add')


@blueprint.route('/transactions/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user == current_user or current_user.is_administrator():
        Transaction.revert(transaction)
        db.session.delete(transaction)
        db.session.commit()
        flash('Transação excluída com sucesso.')
        return redirect(url_for('.list_transactions'))
    else:
        abort(403)


@blueprint.route('/export/<string:table>')
@login_required
@permission_required(Permission.VIEW)
def export(table):
    response = export_table(table, table + '.csv')
    return response
