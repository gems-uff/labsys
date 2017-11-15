from datetime import datetime

from sqlalchemy import asc, desc, UniqueConstraint

from ..extensions import db
from labsys.auth.models import User


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # TODO: make query object
    """
    def query(self, obj):
        for each attribute in self and obj
        if attribute in obj is not null
            compare with attribute
    """


class TimeStampedModelMixin(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    __tablename__ = 'products'

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    # Columns
    name = db.Column(db.String(128), nullable=False)
    stock_minimum = db.Column(db.Integer, default=1, nullable=False)
    # Relationships
    specifications = db.relationship(
        'Specification', backref='product')


class Specification(Base):
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
    products = db.relationship('StockProduct', backref='stock')

    def get_in_stock(self, product):
        for stock_product in self.products:
            if stock_product.compare(product):
                return stock_product
        return None

    def add_product(self, product, lot_number, expiration_date, amount):
        stock_product = StockProduct(self, product, lot_number,
                                     expiration_date, amount)
        in_stock = self.get_in_stock(stock_product)
        if in_stock is None:
            stock_product.create()
        else:
            stock_product.add(amount * product.units)


class StockProduct(Base):
    __tablename__ = 'stock_products'
    __table_args__ = (UniqueConstraint(
        'specification_id', 'stock_id', 'lot_number', name='product_lot'), )

    def __init__(self, stock, specification, lot_number, expiration_date,
                 amount=0, **kwargs):
        super().__init__(**kwargs)
        self.stock = stock
        self.specification = specification
        self.lot_number = lot_number
        self.expiration_date = expiration_date
        self.amount = amount if amount > 0 else 0

    def compare(self, other):
        if self.specification == other.specification and \
           self.lot_number == other.lot_number:
            return True
        return False

    # Columns
    specification_id = db.Column(
        db.Integer, db.ForeignKey('specifications.id'), nullable=False)
    stock_id = db.Column(
        db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    lot_number = db.Column(db.String(64), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, default=0, nullable=False)
    # Relationships
    specification = db.relationship('Specification')


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
    # Relationships
    items = db.relationship(
        'OrderItem', backref='order', cascade='all, delete-orphan')
    # lazy=True: accessing orders will load them from db (user.orders)
    user = db.relationship(
        User, backref=db.backref('orders', lazy=True))


class Transaction(Base, TimeStampedModelMixin):
    __tablename__ = 'transactions'
    # Columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, default=1, nullable=False)
    transaction_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    # Relationships
    user = db.relationship(
        User, backref=db.backref('transactions', lazy=True))
