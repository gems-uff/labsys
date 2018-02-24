import datetime as dt
from factory import PostGenerationMethodCall, Sequence, SubFactory, fuzzy

from labsys.extensions import db
from labsys.inventory.models import (
    Product, StockProduct, Stock, Specification
)
from tests.factories import BaseFactory


class StockFactory(BaseFactory):

    class Meta:
        model = Stock
        abstract = False

    name = Sequence(lambda n: 'stock-{}'.format(n))
    stock_products = []


class SpecificationFactory(BaseFactory):

    class Meta:
        model = Specification
        abstract = False

    manufacturer = 'Manufacturer'
    catalog_number = '123123'
    units = 1


class ProductFactory(BaseFactory):

    class Meta:
        model = Product
        abstract = False
        inline_args = ('name', 'specification')

    specification = SubFactory(SpecificationFactory)
    name = Sequence(lambda n: 'product-{}'.format(n))
    stock_minimum = 1


class StockProductFactory(BaseFactory):

    class Meta:
        model = StockProduct
        abstract = False

    stock = SubFactory(StockFactory)
    product = SubFactory(ProductFactory)
    lot_number = Sequence(lambda n: 'lot-{}'.format(n))
    expiration_date = fuzzy.FuzzyDate(
        dt.date.today(),
        dt.date.today() + dt.timedelta(days=10))
