import pytest
from unittest.mock import MagicMock, patch
from tests.test_inventory.factories import (
    StockProductFactory, StockFactory, SpecificationFactory, ProductFactory,
)
from labsys.inventory.models import StockProduct, Stock


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
            - product is None
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
        stock_product = None
        assert stock.get_in_stock(stock_product) is None

    def test_has_enough(self):
        '''
        Edge cases:
            - in_stock is None and amount is not < amount: return False
            - in_stock is None and amount is < amount: False
            - in_stock is not None and in_stock.amount < amount: False
            - in_stock is not None and in_stock.amount is not < amount: True
        '''
        stock = StockFactory()
        stock_product = StockProductFactory(amount=10)
        with patch.object(Stock, 'get_in_stock', return_value=None):
            assert stock.has_enough(stock_product, 11) is False
            assert stock.has_enough(stock_product, 1) is False
        with patch.object(Stock, 'get_in_stock', return_value=stock_product):
            assert stock.has_enough(stock_product, 11) is False
            assert stock.has_enough(stock_product, 10) is True
        with pytest.raises(ValueError) as excinfo:
            stock.has_enough(stock_product, 0)
        assert 'Amount must be greater than 0' in str(excinfo)

    def test_add_to_stock(self):
        '''
        Edge cases:
            - get_in_stock is None
                - mock stock_product.create()
            - get_in_stock is NOT None
                - mock stock_product.add(value)
                - check if value = amount * product.units
        '''
        stock_product = StockProductFactory()
        with patch.object(Stock, 'get_in_stock', return_value=None):
            pass

    def test_subtract_from_stock(self):
        pass
        '''
        Edge cases:
        '''
