import logging
import sqlalchemy
import jsonpickle

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
    Transaction, Product, Stock, StockProduct, Specification, OrderItem, Order,
)

import labsys.inventory.services as services
import labsys.inventory.forms as forms

blueprint = Blueprint('inventory', __name__)


@blueprint.route('/', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def index():
    return render_template('inventory/index.html')


@blueprint.route('/catalog', methods=['GET'])
@login_required
@permission_required(Permission.VIEW)
def list_catalog():
    products = Product.query.all()
    return render_template('inventory/list-products.html', products=products)


@blueprint.route('/orders/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def purchase_product():
    logging.info('purchase_product()')
    specifications = Specification.query.all()
    form_context = {
        'specs': specifications,
    }
    form = forms.OrderItemForm(**form_context)
    if session.get('order_items') is None:
        session['order_items'] = []

    if request.method == 'POST':
        logging.info('POSTing to purchase_product')
        if form.finish_order.data is True:
            logging.info('checking if there is at least 1 o_item in session')
            if len(session.get('order_items')) > 0:
                logging.info('Finishing order => redirect to checkout()')
                return redirect(url_for('.checkout'))
            logging.info('None order item added to session')
            flash('Pelo menos 1 reativo deve ser adicionado ao carrinho.')
            return redirect(url_for('.purchase_product'))
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
            flash('Reativo adicionado ao carrinho')
            return redirect(url_for('.purchase_product'))
        logging.info('redirecting to route with or w/out errors and form')
    logging.info('GETting purchase_product')
    return render_template('inventory/create-order.html', form=form)


@blueprint.route('/orders/checkout', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def checkout():
    '''
    OK 1. Get order_items from session (jsonpickle)
    OK 2. Create a new Order with order_items
    N-OK 3. Start a new db.transaction
    OK 4. commit the transaction
    OK 5. Add option to cancel the order (resets session, goes back to index, flash)
    OK 6. redirect to stock and flash success message
    OK 7. Show items in cart
    '''
    form = forms.OrderForm()
    order_items = [jsonpickle.decode(item)
                   for item in session.get('order_items')]
    for order_item in order_items:
        order_item.item = Specification.query.get(order_item.item_id)
    logging.info('Retrieve unpickled order_items from session')
    if request.method == 'POST':
        logging.info('POSTing to checkout')
        if form.cancel.data is True:
            logging.info('Cancel order, cleaning session')
            session['order_items'] = []
            return redirect(url_for('.purchase_product'))
        if len(order_items) > 0:
            if form.validate():
                logging.info('starting check out...')
                stock = Stock.query.first()
                order = Order()
                logging.info('populating order with form data and order_items...')
                form.populate_obj(order)
                order.items = order_items
                order.user = current_user
                db.session.add(order)
                db.session.commit()
                try:
                    logging.info('Saving order to database...')
                    order.execute(stock)
                    logging.info('Flashing success and returning to index')
                    flash('Ordem executada com sucesso')
                    session['order_items'] = []
                    return redirect(url_for('.index'))
                except Exception:
                    logging.error('Could not save the order to database.')
                    flash('Algo deu errado, contate um administrador!')
                    return render_template('inventory/index.html')
        else:
            logging.info('No item added to cart')
            flash('É necessário adicionar pelo menos 1 item ao carrinho.')
            return redirect(url_for('.purchase_product'))
    return render_template('inventory/checkout.html',
                           form=form,
                           order_items=order_items,)


@blueprint.route('/products/consume', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def consume_product():
    logging.info('consume_product()')
    # TODO: move this to services
    stock = Stock.query.first()
    stock_products = [sp for sp in stock.stock_products if sp.amount > 0]
    form_context = {
        'stock_products': stock_products,
    }
    form = forms.ConsumeProductForm(**form_context)

    if form.validate_on_submit():
        logging.info('POSTing a valid form to consume_product')
        logging.info('Creating a new SUB Transaction')
        try:
            selected_stock_product = StockProduct.query.get(
                form.stock_product_id.data)
            services.create_sub_transaction(
                current_user,
                selected_stock_product.product,
                selected_stock_product.lot_number,
                form.amount.data,
                stock
            )
            flash('{} unidades de {} removidas do estoque com sucesso!'.format(
                form.amount.data, selected_stock_product.product.name))

            return redirect(url_for('.consume_product'))
        except ValueError as _:
            form.amount.errors.append(
                'Não há o suficiente desse reativo em estoque.')
        except:
            flash('Erro inesperado, contate o administrador.')

    return render_template('inventory/consume-product.html', form=form)


@blueprint.route('/products/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def add_product_to_catalog():
    form = forms.AddProductForm()

    if form.validate_on_submit():
        try:
            specification = Specification(
                form.catalog_number.data,
                form.manufacturer.data,
                form.units.data,
            )
            product = Product(
                name=form.name.data,
                stock_minimum=form.stock_minimum.data,
                specification=specification,
            )
            db.session.add(product)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Já existe uma especificação com esse catálogo e fabricante')
            return render_template('inventory/create-product.html', form=form)
        except Exception as exc:
            db.session.rollback()
            print(exc)
            flash('Ocorreu um erro inesperado, contate um admministrador.')
            return render_template('inventory/create-product.html', form=form)
        return render_template('inventory/details-product.html',
                               product=product)
    return render_template('inventory/create-product.html', form=form)


@blueprint.route('/products/<product_id>/specifications',
                 methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def add_specification_to_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = forms.AddSpecificationForm(product.id)

    if form.validate_on_submit():
        try:
            specification = Specification(
                form.catalog_number.data,
                form.manufacturer.data,
                form.units.data,
            )
            specification.product_id = product_id
            db.session.add(specification)
            db.session.commit()
            flash('Especificação adicionada com sucesso.')
            return redirect(url_for('.detail_product', product_id=product.id))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Já existe uma especificação com esse catálogo e fabricante')
    return render_template('inventory/create-specification.html',
                           form=form, product=product)


@blueprint.route('/products/<product_id>', methods=['GET'])
@login_required
@permission_required(Permission.EDIT)
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('inventory/details-product.html', product=product)


@blueprint.route('/export/<string:table>')
@login_required
@permission_required(Permission.VIEW)
def export(table):
    response = export_table(table, table + '.csv')
    return response
