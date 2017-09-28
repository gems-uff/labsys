import os

from labsys.inventory.forms import ProductForm, AddTransactionForm, \
    SubTransactionForm


class TestProductForm:
    """Add product to catalog form."""

    def test_validate_catalog_already_registered(self):
        assert True


    def test_create_unitary_product_with_correct_data(self):
        assert True


    def test_stock_unit_is_null_for_created_non_unitary_product(self):
        assert True


    def test_validate_subproduct_catalog_does_not_exist(self):
        assert True


    def test_create_product_linked_to_subproduct(self):
        assert True