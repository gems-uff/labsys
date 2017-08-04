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
from ..models import (Transaction, Product, StockProduct)
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
        transaction = Transaction(user=current_user)
        form.populate_obj(transaction)
        catalog_product = Product.query.get(transaction.product_id)
        # Unitary product
        if catalog_product.is_unitary:
            transaction.stock_product = StockProduct.query.filter_by(
                product_id=catalog_product.id,
                allotment=form.allotment.data).first()
            if transaction.stock_product is None:
                transaction.stock_product = StockProduct(
                    product_id=catalog_product.id,
                    allotment=form.allotment.data,
                    amount=transaction.amount, )
            else:
                transaction.stock_product.amount += transaction.amount
        # Non-Unitary => convert parent to child
        else:
            product_id = catalog_product.subproduct.id
            transaction.stock_product = StockProduct.query.filter_by(
                product_id=product_id, allotment=form.allotment.data).first()
            if transaction.stock_product is None:
                transaction.stock_product = StockProduct(
                    product_id=product_id,
                    allotment=form.allotment.data,
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
def create_sub_transaction():
    form = SubTransactionForm()
    form.stock_product_id.choices = [
        (sp.id, sp.product.name + ' Lote: ' + sp.allotment)
        for sp in StockProduct.get_products_in_stock()
    ]
    if form.validate_on_submit():
        allotment = StockProduct.query.get(form.stock_product)
        transaction = Transaction(
            product_allotment=form.allotment.data,
            product_id=form.stock_product_id.data,
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
