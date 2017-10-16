import os

import pytest

from labsys.inventory.forms import ProductForm, AddTransactionForm, \
    SubTransactionForm


@pytest.mark.usefixtures('db')
class TestProductForm:
    """Add product to catalog form."""

    @pytest.mark.skip()
    def test_validate_catalog_already_registered(self):
        assert False

    @pytest.mark.skip()
    def test_create_unitary_product_with_correct_data(self):
        assert False

    @pytest.mark.skip()
    def test_stock_unit_is_null_for_created_non_unitary_product(self):
        assert False

    @pytest.mark.skip()
    def test_validate_subproduct_catalog_does_not_exist(self):
        assert False

    @pytest.mark.skip()
    def test_create_product_linked_to_subproduct(self):
        assert False

    @pytest.mark.skip()
    def test_non_unitary_but_no_subproduct_input(self):
        assert False

    @pytest.mark.skip()
    def test_min_stock_is_zero_for_non_unitary(self):
        assert False