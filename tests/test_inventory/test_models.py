import pytest

from tests.test_inventory.factories import (
    StockProductFactory, StockFactory, SpecificationFactory, ProductFactory,
)


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


class TestStock:
    def test_get_in_stock(self):
        '''
        Edge cases:
            - self.products is None => None
            - self.products is not None but prod.compare is False => None
            - self.products is not None and prod.compare is True => prod
        '''
        pass

    def test_add_product(self):
        '''
        Edge cases:
            - get_in_stock is None
                - mock stock_product.create()
            - get_in_stock is NOT None
                - mock stock_product.add(value)
                - check if value = amount * product.units
        '''
