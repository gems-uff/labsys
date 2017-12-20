import jsonpickle
from datetime import datetime

from sqlalchemy import asc, desc, UniqueConstraint, CheckConstraint

from ..extensions import db
from .services import create_add_transaction_from_order
from labsys.auth.models import User


ADD = 1
SUB = 2


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # TODO: make query object
    """
    def query(self, obj):
        for each attribute in self and obj
        if attribute in obj is not null
            compare with attribute
    """
    def toJSON(self):
        return jsonpickle.encode(self)


class TimeStampedModelMixin(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    __tablename__ = 'products'

    def __init__(self, name, specification, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.specifications.append(specification)

    def __str__(self):
        return self.name

    # Columns
    name = db.Column(db.String(128), nullable=False)
    stock_minimum = db.Column(db.Integer, default=1, nullable=False)
    # Relationships
    specifications = db.relationship(
        'Specification', backref='product')

    def get_base_spec(self):
        if len(self.specifications) > 0:
            return self.specifications[0]
        return None


class Specification(Base):

    def __init__(self, catalog_number, manufacturer, units=1, **kwargs):
        super().__init__(**kwargs)
        self.catalog_number = catalog_number
        self.manufacturer = manufacturer
        self.units = units

    __tablename__ = 'specifications'
    __table_args__ = (UniqueConstraint(
        'manufacturer', 'catalog_number', name='manufacturer_catalog'), )
    # Columns
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=False)
    manufacturer = db.Column(db.String(128), nullable=False)
    catalog_number = db.Column(db.String(128), nullable=False)
    units = db.Column(db.Integer, default=1, nullable=False)


class Stock(Base):
    __tablename__ = 'stocks'
    # Columns
    name = db.Column(db.String(128), nullable=False)
    # Relationships
    stock_products = db.relationship('StockProduct', backref='stock')

    def get_in_stock(self, product, lot_number):
        for stock_product in self.stock_products:
            other_stock_product = StockProduct(
                None, product, lot_number, None)
            if stock_product.compare(other_stock_product):
                return stock_product
        return None

    def has_enough(self, product, lot_number, amount):
        if amount < 1:
            raise ValueError('Amount must be greater than 0')
        in_stock = self.get_in_stock(product, lot_number)
        if in_stock is None or in_stock.amount < amount:
            return False
        return True

    def total(self, product):
        total = 0
        for sp in self.stock_products:
            if sp.product_id == product.id:
                total += sp.amount
        return total

    def add(self, product, lot_number, expiration_date, amount):
        """
        amount: total units to be added
        """
        if amount < 1 or isinstance(amount, int) is False:
            raise ValueError('Amount must be a positive integer')
        stock_product = self.get_in_stock(product, lot_number)
        if stock_product is None:
            stock_product = StockProduct(
                self, product, lot_number, expiration_date)
        stock_product.amount += amount
        return True

    def subtract(self, product, lot_number, amount):
        """
        amount: total units to be subtracted
        """
        if amount < 1 or isinstance(amount, int) is False:
            raise ValueError('Amount must be a positive integer')
        in_stock = self.get_in_stock(product, lot_number)
        if in_stock is None:
            raise ValueError('There is no {} in stock'.format(product.name))
        if self.has_enough(product, lot_number, amount):
            in_stock.amount -= amount
            return True
        raise ValueError('Not enough in stock')


class StockProduct(Base):
    __tablename__ = 'stock_products'
    __table_args__ = (UniqueConstraint(
        'product_id', 'stock_id', 'lot_number', name='stock_product'), )

    def __init__(self, stock, product, lot_number, expiration_date,
                 amount=0, **kwargs):
        super().__init__(**kwargs)
        self.stock = stock
        self.product = product
        self.lot_number = lot_number
        self.expiration_date = expiration_date
        self.amount = amount if amount > 0 else 0

    # Columns
    stock_id = db.Column(
        db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=False)
    lot_number = db.Column(db.String(64), nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Integer, default=0, nullable=False)
    # Relationships
    product = db.relationship('Product')

    def compare(self, other):
        if self.product == other.product \
               and self.lot_number == other.lot_number:
            return True
        return False


class OrderItem(Base):
    __tablename__ = 'order_items'
    __tableargs__ = (UniqueConstraint(
        'item_id', 'order_id', name='order_item'), )
    # Columns
    item_id = db.Column(
        db.Integer, db.ForeignKey('specifications.id'), nullable=False)
    order_id = db.Column(
        db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Integer, default=1, nullable=False)
    lot_number = db.Column(db.String(64), nullable=False)
    expiration_date = db.Column(
        db.Date, default=datetime.utcnow().date, nullable=True)
    # Relationships
    item = db.relationship(Specification)


class Order(Base, TimeStampedModelMixin):
    __tablename__ = 'orders'
    # Columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    invoice = db.Column(db.String(128), nullable=True)
    invoice_type = db.Column(db.String(128), nullable=True)
    financier = db.Column(db.String(128), nullable=True)
    notes = db.Column(db.String(256), nullable=True)
    order_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    executed = db.Column(db.Boolean, default=False, nullable=False)
    # Relationships
    items = db.relationship(
        OrderItem, backref='order', cascade='all, delete-orphan')
    # lazy=True: accessing orders will load them from db (user.orders)
    user = db.relationship(
        User, backref=db.backref('orders', lazy=True))

    def execute(self, stock):
        if not self.executed:
            create_add_transaction_from_order(self, stock)
            self.executed = True
            db.session.add(self)
            db.session.commit()
        else:
            raise ValueError('Order has already been executed')


class Transaction(Base, TimeStampedModelMixin):
    __tablename__ = 'transactions'
    # Columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=False)
    stock_id = db.Column(
        db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    # TODO: make sure alembic migrations recognizes this
    __table_args__ = (
        CheckConstraint(amount > 0, name='amount_is_positive'), {})

    # Relationships
    user = db.relationship(
        User, backref=db.backref('transactions', lazy=True))
    product = db.relationship(
        Product, backref=db.backref('transactions', lazy=True))
    stock = db.relationship(
        Stock, backref=db.backref('transactions', lazy=True))

    def __init__(self, user, product, lot_number, amount, stock, category,
                 expiration_date=None):
        self.user = user
        self.product = product
        self.amount = amount
        self.stock = stock
        self.category = category

        if category is ADD:
            stock.add(
                product,
                lot_number,
                expiration_date,
                amount,
            )
        else:
            sub = stock.subtract(product, lot_number, amount)
            if sub is not True:
                # raise sub
                raise ValueError('Could not subtract from stock')
