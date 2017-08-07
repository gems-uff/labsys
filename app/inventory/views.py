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
from .forms import AddTransactionForm, SubTransactionForm, ProductForm


@inventory.route('/', methods=['GET'])
def index():
    return render_template('inventory/index.html')


@inventory.route('/reactives', methods=['GET'])
def list_products():
    return render_template('inventory/list-products.html')


@inventory.route('/reactives/add', methods=['GET', 'POST'])
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
        (sp.id, sp.product.name + ' | Lote: ' + sp.allotment +
         ' | {} unidades.'.format(sp.amount))
        for sp in StockProduct.get_products_in_stock()
    ]
    if form.validate_on_submit():
        allotment = StockProduct.query.get(
            form.stock_product_id.data).allotment
        transaction = Transaction(user=current_user)
        form.populate_obj(transaction)
        transaction.stock_product = StockProduct.query.get(
            transaction.stock_product_id)
        # transaction.amount is negative (form changes its sign)
        transaction.stock_product.amount += transaction.amount
        transaction.product = transaction.stock_product.product
        db.session.add(transaction)
        db.session.commit()
        flash('Baixa realizada com sucesso.')
        return redirect(url_for('.create_sub_transaction', method='sub'))

    return render_template(
        'inventory/create-transaction.html', form=form, method='sub')
