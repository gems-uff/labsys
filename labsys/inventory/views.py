import jsonpickle
import sqlalchemy
from flask import (current_app, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user

from labsys.auth.decorators import permission_required
from labsys.auth.models import Permission
from labsys.extensions import db
from labsys.utils.decorators import paginated

from . import blueprint, forms, logger, services, utils
from .models import (Order, OrderItem, Product, Specification, Stock,
                     StockProduct, Transaction)


@blueprint.route('/', methods=['GET'])
@permission_required(Permission.VIEW)
def index():
    return redirect(url_for('.show_stock'))


@blueprint.route('/catalog', methods=['GET'])
@permission_required(Permission.VIEW)
def show_catalog():
    template = 'inventory/list-products.html'
    view = 'inventory.show_catalog'
    query = Product.query.order_by(Product.name)
    context_title = 'products'
    return paginated(
        query=query,
        template_name=template,
        view_method=view,
        context_title=context_title)


@blueprint.route('/stock', methods=['GET'])
@permission_required(Permission.VIEW)
def show_stock():
    stock = Stock.query.first()
    template = 'inventory/index.html'
    products = db.session.query(Product).join(StockProduct).order_by(
        Product.name).all()
    for p in products:
        p.total = stock.total(p)
    return render_template(template, products=products)


@blueprint.route('/transactions', methods=['GET'])
@permission_required(Permission.VIEW)
def list_transactions():
    template = 'inventory/list-transactions.html'
    view = 'inventory.list_transactions'
    query = Transaction.query.order_by(Transaction.updated_on.desc())
    context_title = 'transactions'
    return paginated(
        query=query,
        template_name=template,
        view_method=view,
        context_title=context_title)


@blueprint.route('/orders', methods=['GET'])
@permission_required(Permission.VIEW)
def list_orders():
    template = 'inventory/list-orders.html'
    view = 'inventory.list_orders'
    query = Order.query.order_by(Order.order_date.desc())
    context_title = 'orders'
    return paginated(
        query=query,
        template_name=template,
        view_method=view,
        context_title=context_title)


# TODO: Implement this method:
@blueprint.route('/transactions/<int:transaction_id>/delete', methods=['GET'])
@permission_required(Permission.DELETE)
def delete_transaction(transaction_id):
    flash('Essa funcionalidade ainda não foi implementada.', 'warning')
    return redirect(url_for('.list_transactions'))


@blueprint.route('/orders/add', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def purchase_product():
    logger.info('purchase_product()')
    specifications = db.session.query(Specification).\
        join(Product).\
        order_by(Product.name).\
        all()
    form_context = {
        'specs': specifications,
    }
    form = forms.OrderItemForm(**form_context)

    if session.get('order_items') is None:
        session['order_items'] = []
    order_items = [
        jsonpickle.decode(item) for item in session.get('order_items')
    ]
    for order_item in order_items:
        order_item.item = Specification.query.get(order_item.item_id)

    if request.method == 'POST':
        logger.info('POSTing to purchase_product')
        if form.cancel.data is True:
            logger.info('Cancel order, cleaning session')
            session['order_items'] = []
            return redirect(url_for('.purchase_product'))
        if form.finish_order.data is True:
            logger.info('checking if there is at least 1 o_item in session')
            if len(session.get('order_items')) > 0:
                logger.info('Finishing order => redirect to checkout()')
                return redirect(url_for('.checkout'))
            logger.info('None order item added to session')
            flash('Pelo menos 1 reativo deve ser adicionado ao carrinho.',
                  'danger')
            return redirect(url_for('.purchase_product'))
        if form.validate():
            logger.info('Create order form is valid')
            order_item = OrderItem()
            form.populate_obj(order_item)
            logger.info('order_item obj was populated')
            if len(session.get('order_items')) is 0:
                logger.info('order_items not found in session => create [oi]')
                session['order_items'] = [order_item.toJSON()]
            else:
                logger.info('order_items found in session => append(oi)')
                session['order_items'].append(order_item.toJSON())
                # See http://flask.pocoo.org/docs/0.12/api/#sessions
                # Must be manually set
                session.modified = True

            logger.info('finishing form.validate')
            flash('Reativo adicionado ao carrinho', 'success')
            return redirect(url_for('.purchase_product'))
        logger.info('redirecting to route with or w/out errors and form')
    logger.info('GETting purchase_product')
    return render_template(
        'inventory/create-order.html', form=form, order_items=order_items)


@blueprint.route('/orders/checkout', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def checkout():
    form = forms.OrderForm()
    stock = Stock.get_reactive_stock()
    if session.get('order_items') is None:
        session['order_items'] = []
    order_items = [
        jsonpickle.decode(item) for item in session.get('order_items')
    ]
    for order_item in order_items:
        order_item.item = Specification.query.get(order_item.item_id)
    logger.info('Retrieve unpickled order_items from session')
    if request.method == 'POST':
        logger.info('POSTing to checkout')
        if form.cancel.data is True:
            logger.info('Cancel order, cleaning session')
            session['order_items'] = []
            return redirect(url_for('.purchase_product'))
        if len(order_items) > 0:
            if form.validate():
                logger.info('starting check out...')
                order = Order()
                logger.info('populating order with form data and order_items')
                form.populate_obj(order)
                order.items = order_items
                order.user = current_user
                db.session.add(order)
                try:
                    logger.info('Saving order to database...')
                    for order_item in order.items:
                        logger.info('Adding %s to stock' % order_item)
                        product = order_item.item.product
                        lot_number = order_item.lot_number
                        total_units = order_item.amount * order_item.item.units
                        expiration_date = order_item.expiration_date
                        logger.info('stock.add({}, {}, {}, {})'.format(
                            product, lot_number, expiration_date, total_units))
                        stock.add(product, lot_number, expiration_date,
                                  total_units)
                        order_item.added_to_stock = True
                        db.session.add(order_item)
                    logger.info('Comitting session...')
                    db.session.commit()
                    logger.info('Creating transactions from order...')
                    services.create_add_transaction_from_order(order, stock)
                    logger.info('Flashing success and returning to index')
                    flash('Ordem executada com sucesso', 'success')
                    session['order_items'] = []
                    return redirect(url_for('.index'))
                except (ValueError, Exception) as err:
                    db.session.rollback()
                    session['order_items'] = []
                    logger.error('Could not save the order to db. Rollback.')
                    logger.error(err)
                    flash('Algo deu errado, contate um administrador!')
                    return render_template('inventory/index.html')
        else:
            logger.info('No item added to cart')
            flash('É necessário adicionar pelo menos 1 item ao carrinho.',
                  'warning')
            return redirect(url_for('.purchase_product'))
    return render_template(
        'inventory/checkout.html',
        form=form,
        order_items=order_items,
    )


@blueprint.route('/products/consume', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def consume_product():
    logger.info('consume_product()')
    stock = Stock.get_reactive_stock()
    stock_products = sorted(
        [sp for sp in stock.stock_products if sp.amount > 0],
        key=lambda sp: sp.product.name,
    )
    # sorted(student_tuples, key=lambda student: student[2])
    form_context = {
        'stock_products': stock_products,
    }
    form = forms.ConsumeProductForm(**form_context)

    if form.validate_on_submit():
        logger.info('POSTing a valid form to consume_product')
        logger.info('Creating a new SUB Transaction')
        try:
            selected_stock_product = StockProduct.query.get(
                form.stock_product_id.data)
            logger.info('Retrieving info from selected_stock_product')
            product = selected_stock_product.product
            lot_number = selected_stock_product.lot_number
            amount = form.amount.data
            stock.subtract(product, lot_number, amount)
            logger.info('Commiting subtraction')
            db.session.commit()
            logger.info('Creating sub-transaction')
            services.create_sub_transaction(current_user, product, lot_number,
                                            amount, stock)
            flash(
                '{} unidades de {} removidas do estoque com sucesso!'.format(
                    form.amount.data, selected_stock_product.product.name),
                'success')

            return redirect(url_for('.consume_product'))
        except ValueError as err:
            logger.error(err)
            form.amount.errors.append(
                'Não há o suficiente desse reativo em estoque.')
        except Exception:
            flash('Erro inesperado, contate o administrador.', 'danger')

    return render_template('inventory/consume-product.html', form=form)


@blueprint.route('/products/add', methods=['GET', 'POST'])
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
            db.session.add(specification)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Já existe uma especificação com esse catálogo e fabricante',
                  'danger')
            return render_template('inventory/create-product.html', form=form)
        except Exception as exc:
            db.session.rollback()
            logger.info(exc)
            flash('Ocorreu um erro inesperado, contate um admministrador.',
                  'danger')
            return render_template('inventory/create-product.html', form=form)
        return redirect(
            url_for(
                '.detail_product',
                product_id=product.id,
                specifications=product.specifications))
    return render_template('inventory/create-product.html', form=form)


@blueprint.route(
    '/products/<int:product_id>/specifications', methods=['GET', 'POST'])
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
            flash('Especificação adicionada com sucesso.', 'success')
            return redirect(url_for('.detail_product', product_id=product.id))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Já existe uma especificação com esse catálogo e fabricante',
                  'danger')
    return render_template(
        'inventory/create-specification.html', form=form, product=product)


@blueprint.route('/products/<int:product_id>', methods=['GET'])
@permission_required(Permission.EDIT)
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)
    specifications = sorted(
        [spec for spec in product.specifications],
        key=lambda spec: spec.units,
    )
    return render_template(
        'inventory/details-product.html',
        product=product,
        specifications=specifications)


@blueprint.route('/export/<string:table>')
@permission_required(Permission.VIEW)
def export(table):
    response = utils.export_table(table, table + '.csv')
    return response
