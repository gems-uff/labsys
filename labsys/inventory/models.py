from datetime import datetime

from sqlalchemy import asc, desc, UniqueConstraint

from ..extensions import db


class Product(db.Model):
    # TODO: change parent_id to child_id in order to not allow a product to have
    # more than one type of subproduct
    __tablename__ = 'products'
    __table_args__ = (UniqueConstraint(
        'manufacturer', 'catalog', name='catalog_product'), )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    manufacturer = db.Column(db.String(128))
    catalog = db.Column(db.String(128))
    stock_unit = db.Column(db.Integer, default=1)
    min_stock = db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    subproduct = db.relationship(
        'Product', backref='parent', uselist=False, remote_side=[id])
    transactions = db.relationship(
        'Transaction', backref='product', lazy='dynamic')
    stock_products = db.relationship(
        'StockProduct', backref='product', lazy='dynamic')

    @property
    def is_unitary(self):
        return self.stock_unit == 1

    @property
    def unit_product(self):
        if self.is_unitary:
            return self
        else:
            return self.subproduct

    @classmethod
    def get_products(cls, unitary_only=False):
        products = cls.query.order_by(asc(cls.catalog)).all()
        if unitary_only:
            return [p for p in products if p.is_unitary]
        return products

    @classmethod
    def get_products_by_manufacturer(cls, manufacturer, unitary_only=False):
        products = cls.query.order_by(asc(cls.name)).filter_by(
            manufacturer=manufacturer).all()
        if unitary_only:
            return [p for p in products if p.is_unitary]
        return products

    @classmethod
    def get_product_by_catalog(cls, catalog, unitary_only=False):
        products = cls.query.order_by(asc(cls.name)).filter_by(
            catalog=catalog).first()
        if unitary_only:
            return [p for p in products if p.is_unitary]
        return products

    def count_amount_stock_products(self):
        amount_in_stock = 0
        for stock_product in self.stock_products:
            amount_in_stock += stock_product.amount

        return amount_in_stock

    def __repr__(self):
        return '<Product[({}) {}], cat: {}>'.format(
            self.id, self.name, self.catalog)

    def __str__(self):
        return '<Product[({}) {}], cat: {}>'.format(
            self.id, self.name, self.catalog)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer, default=0)
    invoice_type = db.Column(db.String(64))
    invoice = db.Column(db.String(64))
    financier = db.Column(db.String(128))
    details = db.Column(db.String(256))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    stock_product_id = db.Column(db.Integer,
                                 db.ForeignKey('stock_products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def get_product_amount(cls, product):
        id = product[0]
        lot_number = product[1]
        return cls.query.filter_by(
            product_id=id, lot_number=lot_number).count()

    @classmethod
    def get_transactions_ordered(cls):
        return cls.query.order_by(desc(cls.transaction_date)).all()

    def receive_product(self, lot_number, expiration_date=None):
        self.product = Product.query.get(self.product_id)
        self.stock_product = StockProduct.query.filter_by(
            product_id=self.product.unit_product.id,
            lot_number=lot_number).first()
        # First product of this lot added => create a new StockProduct
        if self.stock_product is None:
            self.stock_product = StockProduct(
                product_id=self.product.unit_product.id, amount=0)
        # There's already one product of this lot => Add to its amount only
        # Or update it
        self.stock_product.amount += self.product.stock_unit * self.amount
        self.stock_product.lot_number = lot_number
        self.stock_product.expiration_date = expiration_date or \
                                             self.expiration_date

    def consume_product(self):
        # I just need the product of a consume transaction
        # to show it in the stock view
        self.stock_product = StockProduct.query.get(self.stock_product_id)
        self.product = self.stock_product.product
        self.stock_product.amount += self.amount

    @classmethod
    def revert(cls, transaction):
        transaction.stock_product.amount -= (
            transaction.amount * transaction.product.stock_unit)
        transaction.amount = 0
        if transaction.stock_product.amount == 0:
            StockProduct.erase_depleted()

    def __repr__(self):
        return '{} : {}'.format(self.id, self.transaction_date)


class StockProduct(db.Model):
    __tablename__ = 'stock_products'
    __table_args__ = (UniqueConstraint(
        'product_id', 'lot_number', name='stock_product'), )
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    lot_number = db.Column(db.String(64), nullable=False)
    expiration_date = db.Column(db.Date(), nullable=False)
    amount = db.Column(db.Integer)
    transactions = db.relationship(
        'Transaction', backref='stock_product', lazy='dynamic')

    def __repr__(self):
        return '<StockProduct[{}]: {}, lote {}>'.format(
            self.id, self.product.name[:10], self.lot_number)

    @classmethod
    def total_amount_in_stock(cls, stock_product):
        # TODO: implement
        pass

    @classmethod
    def list_products_in_stock(cls):
        stock_products = cls.query.filter(cls.amount > 0).all()

        return sorted(
            stock_products,
            key=
            lambda stock_product: (stock_product.product.catalog, stock_product.expiration_date)
        )

    @classmethod
    def erase_depleted(cls):
        """Erase all lots of stock products which amount is zero"""
        for sp in cls.query.all():
            if sp.amount == 0:
                db.session.delete(sp)
        db.session.commit()
