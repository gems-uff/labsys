import logging, jsonpickle

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
def purchase_product():
    logging.info('purchase_product()')
    products = Product.query.all()
    specifications = Specification.query.all()
    form_context = {
        'products': products,
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
            flash('Pelo menos 1 produto deve ser adicionado ao carrinho.')
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
            flash('Produto adicionado ao carrinho')
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
    '''
    - Retrieve all products and stock_products
    - Show consume form
    -
    '''
    logging.info('consume_product()')
    # TODO: move this to services
    stock = Stock.query.first()
    products = [p for p in Product.query.join(
                    StockProduct, Product.id==StockProduct.product_id)
                    .filter(StockProduct.stock_id==stock.id)]
    stock_products = [sp for sp in stock.stock_products]
    lot_numbers = [sp.lot_number for sp in stock.stock_products]
    form_context = {
        'products': products,
        'stock_products': stock_products,
        'lot_numbers': lot_numbers,
    }
    form = forms.ConsumeProductForm(**form_context)
    return render_template('inventory/consume-product.html', form=form)


@blueprint.route('/products/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def add_product():
    '''
    1. Render the add product/spec form
    '''
    return 'oi'


@blueprint.route('/export/<string:table>')
@login_required
@permission_required(Permission.VIEW)
def export(table):
    response = export_table(table, table + '.csv')
    return response
