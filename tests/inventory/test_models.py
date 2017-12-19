import pytest
from unittest.mock import MagicMock, patch
from tests.inventory.factories import (
    StockProductFactory, StockFactory, ProductFactory,
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
        product = ProductFactory()
        self_stock_product = StockProductFactory(
            product=product,
            lot_number='123'
        )
        other_stock_product = StockProductFactory(
            product=product,
            lot_number='123'
        )
        assert self_stock_product.compare(other_stock_product) is True
        other_stock_product = StockProductFactory(
            product=ProductFactory(),
            lot_number='123'
        )
        assert self_stock_product.compare(other_stock_product) is False
        other_stock_product = StockProductFactory(
            product=product,
            lot_number='321'
        )
        assert self_stock_product.compare(other_stock_product) is False
        other_stock_product = StockProductFactory(
            product=ProductFactory(),
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
            - product is None => return None
        '''
        empty_stock = StockFactory()
        assert empty_stock.get_in_stock(None, 123) is None
        # compare is True
        with patch.object(
                StockProduct, 'compare', return_value=True):
            product = ProductFactory(name='FoundProduct')
            non_empty_stock = StockFactory()
            in_stock = StockProductFactory(
                stock=non_empty_stock, product=product, lot_number=123)
            found_product = non_empty_stock.get_in_stock(product, 123)
            assert found_product is not None
            assert found_product.product.name is 'FoundProduct'
            assert found_product == non_empty_stock.stock_products[0]
        with patch.object(
                StockProduct, 'compare', return_value=False):
            product = ProductFactory()
            non_empty_stock = StockFactory()
            in_stock = StockProductFactory(
                stock=non_empty_stock, product=product, lot_number=123)
            non_empty_stock.get_in_stock(product, 123)
            not_found_product = non_empty_stock.get_in_stock(product, 123)
            assert not_found_product is None

        product = None
        stock = StockFactory()
        assert stock.get_in_stock(product, 123) is None

    def test_has_enough(self):
        '''
        Edge cases:
            - in_stock is None and amount is not < amount: return False
            - in_stock is None and amount is < amount: False
            - in_stock is not None and in_stock.amount < amount: False
            - in_stock is not None and in_stock.amount is not < amount: True
        '''
        product = ProductFactory(name='Find me')
        stock = StockFactory()
        stock_product = StockProductFactory(
            stock=stock, product=product, amount=10)
        lot_number = 123
        with patch.object(Stock, 'get_in_stock', return_value=None):
            assert stock.has_enough(product, lot_number, 11) is False
            assert stock.has_enough(product, lot_number, 1) is False
        with patch.object(Stock, 'get_in_stock', return_value=stock_product):
            assert stock.has_enough(product, lot_number, 11) is False
            assert stock.has_enough(product, lot_number, 10) is True
        with pytest.raises(ValueError) as excinfo:
            stock.has_enough(product, lot_number, 0)
        assert 'Amount must be greater than 0' in str(excinfo)

    def test_add_to_stock(self):
        stock = StockFactory()
        product = ProductFactory()
        with patch.object(Stock, 'get_in_stock', return_value=None):
            assert len(stock.stock_products) is 0
            assert stock.add(product, 123, None, 10) is True
            assert stock.stock_products[0].amount is 10
            assert len(stock.stock_products) is 1
        with patch.object(
                Stock, 'get_in_stock', return_value=stock.stock_products[0]):
            assert len(stock.stock_products) is 1
            assert stock.add(product, 123, None, 10) is True
            assert stock.stock_products[0].amount is 20
            assert len(stock.stock_products) is 1
        with pytest.raises(ValueError) as excinfo:
            stock = StockFactory()
            stock.add(product, 123, None, amount=0)
        assert 'Amount must be a positive integer' in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            stock = StockFactory()
            stock.add(product, 123, None, amount=1.0)
        assert 'Amount must be a positive integer' in str(excinfo)

    def test_subtract_from_stock(self):
        stock = StockFactory()
        product = ProductFactory()
        stock_product = StockProductFactory(
            stock=stock, product=product, amount=10, lot_number=123)
        with patch.object(Stock, 'get_in_stock', return_value=None):
            with pytest.raises(ValueError) as excinfo:
                stock.subtract(product, 123, 10)
            err_msg = 'There is no {} in stock'.format(product.name)
            assert  err_msg in str(excinfo)
            assert stock_product.amount is 10
        with patch.object(Stock, 'get_in_stock', return_value=stock_product):
            with patch.object(Stock, 'has_enough', return_value=False):
                with pytest.raises(ValueError) as excinfo:
                    stock.subtract(product, 123, 10)
                err_msg = 'Not enough in stock'
                assert err_msg in str(excinfo)
                assert stock_product.amount is 10
            with patch.object(Stock, 'has_enough', return_value=True):
                assert stock.subtract(product, 123, 10) is True
                assert stock_product.amount is 0
        with pytest.raises(ValueError) as excinfo:
            stock = StockFactory()
            product = ProductFactory()
            stock.subtract(product, 123, amount=0)
        assert 'Amount must be a positive integer' in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            stock = StockFactory()
            product = ProductFactory()
            stock.subtract(product, 123, amount=1.0)
        assert 'Amount must be a positive integer' in str(excinfo)
