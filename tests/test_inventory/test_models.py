import pytest
from unittest.mock import MagicMock, patch
from tests.test_inventory.factories import (
    StockProductFactory, StockFactory, SpecificationFactory, ProductFactory,
)
from labsys.inventory.models import StockProduct


@pytest.mark.usefixtures('db')
class TestStockProduct:
    def test_compare(self):
        '''
        Edge cases:
            - specifications AND lot_number match: => True
            - specifications OK lot_number NOK => False
            - speicifcations NOK lot_number OK => False
            - speicifcations NOK lot_number NOK => False
        '''
        specification = SpecificationFactory(product=ProductFactory())
        self_stock_product = StockProductFactory(
            specification=specification,
            lot_number='123'
        )
        other_stock_product = StockProductFactory(
            specification=specification,
            lot_number='123'
        )
        assert self_stock_product.compare(other_stock_product) is True
        other_stock_product = StockProductFactory(
            specification=SpecificationFactory(),
            lot_number='123'
        )
        assert self_stock_product.compare(other_stock_product) is False
        other_stock_product = StockProductFactory(
            specification=specification,
            lot_number='321'
        )
        assert self_stock_product.compare(other_stock_product) is False
        other_stock_product = StockProductFactory(
            specification=SpecificationFactory(),
            lot_number='123321'
        )
        assert self_stock_product.compare(other_stock_product) is False

    def test_init_amount_default(self):
        '''
        Edge cases:
            - Amount not provided => amount = 0
            - Amount provded => amount = value
            - Amount < 0 => amount = 0
        '''
        stock_product = StockProductFactory()
        assert stock_product.amount is 0
        stock_product = StockProductFactory(amount=10)
        assert stock_product.amount is 10
        stock_product = StockProductFactory()
        assert stock_product.amount is 0


class TestStock:
    def test_get_in_stock(self):
        '''
        Edge cases:
            - self.products is empty => None
            - self.products is not empty and prod.compare is False => None
            - self.products is not empty and prod.compare is True => prod
        '''
        stock = StockFactory()
        stock_product = StockProductFactory()
        stock.products = []
        assert stock.get_in_stock(stock_product) is None
        stock.products.append(StockProductFactory())
        with patch.object(
                StockProduct, 'compare', return_value=False) as mock_compare:
            assert stock.get_in_stock(stock_product) is None
        with patch.object(
                StockProduct, 'compare', return_value=True) as mock_compare:
            found_product = stock.get_in_stock(stock_product)
            assert found_product is not None
            assert found_product == stock.products[0]

    def test_add_product(self):
        '''
        Edge cases:
            - get_in_stock is None
                - mock stock_product.create()
            - get_in_stock is NOT None
                - mock stock_product.add(value)
                - check if value = amount * product.units
        '''
