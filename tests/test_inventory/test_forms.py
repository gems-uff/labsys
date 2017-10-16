import os

import pytest

from labsys.inventory.forms import ProductForm, AddTransactionForm, \
    SubTransactionForm
from labsys.inventory.models import Product
from ..factories import ProductFactory


@pytest.mark.usefixtures('db')
class TestProductForm:

    def test_validate_product_already_registered(self):
        """
        A product is already registered if its catalog and manufacturer already
        exist.
        """
        error_msg = 'Esse produto já está registrado no catálogo!'
        registered_product = ProductFactory(manufacturer='A', catalog='123')
        form = ProductForm(obj=registered_product)

        assert form.validate() is False
        assert len(form.errors) == 1
        assert error_msg in form.catalog.errors

    def test_create_product_same_catalog_but_differente_manufacturer(self, db):
        registered_product = ProductFactory(manufacturer='A', catalog='123')
        form = ProductForm(obj=registered_product)
        form.manufacturer.data = 'A different manufacturer'
        assert form.validate() is True
        product_from_form = Product()
        form.populate_obj(product_from_form)
        db.session.add(product_from_form)
        db.session.commit()
        p = Product.query.filter_by(id = product_from_form.id).all()[0]
        assert p is not None
        assert p.manufacturer == 'A different manufacturer'


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