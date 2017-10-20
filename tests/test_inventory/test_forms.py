import os

import pytest

from wtforms import Field
from wtforms import ValidationError

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

    def test_valid_product_same_catalog_different_manufacturer(self, db):
        registered_product = ProductFactory(manufacturer='A', catalog='123')
        form = ProductForm(obj=registered_product)
        form.manufacturer.data = 'A different manufacturer'
        assert form.validate() is True # this should be enough
        product_from_form = Product()
        # TODO: move this logic to functional tests
        form.populate_obj(product_from_form)
        db.session.add(product_from_form)
        db.session.commit()
        p = Product.query.filter_by(id = product_from_form.id).all()[0]
        assert p is not None
        assert p.manufacturer == 'A different manufacturer'

    def test_validation_subproduct_catalog_is_null_or_empty(self):
        # Empty
        non_unitary_product_form = ProductForm(
            name='Non Unitary', manufacturer='Any Manufacturer', catalog='123',
            stock_unit=1000, min_stock=1, subproduct_catalog=''
        )
        error_msg = 'Subproduto deve ser preenchido ' \
                    'para produtos não unitários.'
        assert non_unitary_product_form.validate() is False
        assert error_msg in non_unitary_product_form.subproduct_catalog.errors
        # None
        non_unitary_product_form = ProductForm(
            name='Non Unitary', manufacturer='Any Manufacturer', catalog='123',
            stock_unit=1000, min_stock=1, subproduct_catalog=None
        )
        error_msg = 'Subproduto deve ser preenchido ' \
                    'para produtos não unitários.'
        assert non_unitary_product_form.validate() is False
        assert error_msg in non_unitary_product_form.subproduct_catalog.errors

    def test_unitary_product_with_subproduct_input(self):
        form = ProductForm(
            name='Non Unitary', manufacturer='Any Manufacturer', catalog='123',
            stock_unit=1, min_stock=1, subproduct_catalog='123'
        )
        assert form.validate() is False
        error_msg = 'Produtos unitários não possuem subproduto.'
        assert error_msg in form.subproduct_catalog.errors

    def test_valid_non_unitary_product_with_subproduct(self):
        subproduct = ProductFactory(catalog='321')
        form = ProductForm(
            name='Non Unitary', manufacturer='Any Manufacturer', catalog='123',
            stock_unit=4, min_stock=1, subproduct_catalog='321'
        )
        assert form.validate() is True

    # Could not test this, validate_subproduct_catalog not being called
    # although it is called via the application
    @pytest.mark.skip()
    def test_subproduct_does_not_exist(self, db):
        form = ProductForm(
            name='Non Unitary', manufacturer='Any Manufacturer', catalog='abc',
            stock_unit=2, min_stock=2, subproduct_catalog='99999'
        )
        assert form.validate() is False
        error_msg = 'Subproduto informado não existe.'
        assert error_msg in form.subproduct_catalog.errors

    def test_validate_subproduct_catalog(self):
        form = ProductForm()
        subproduct_catalog = Field()
        subproduct_catalog.data = ''
        form.validate_subproduct_catalog(subproduct_catalog)
        assert len(form.errors) == 0
        subproduct_catalog.data = None
        form.validate_subproduct_catalog(subproduct_catalog)
        assert len(form.errors) == 0
        subproduct_catalog.data = '123'
        error_msg = 'Subproduto informado não existe.'
        with pytest.raises(ValidationError) as excinfo:
            form.validate_subproduct_catalog(subproduct_catalog)
        assert error_msg in str(excinfo.value)
        product = ProductFactory(catalog='123', stock_unit=2)
        form.manufacturer.data = product.manufacturer
        error_msg = 'Subproduto informado não é unitário.'
        with pytest.raises(ValidationError) as excinfo:
            form.validate_subproduct_catalog(subproduct_catalog)
        assert error_msg in str(excinfo.value)

    @pytest.mark.skip()
    def test_create_product_linked_to_subproduct(self):
        assert False

    @pytest.mark.skip()
    def test_non_unitary_but_no_subproduct_input(self):
        assert False

    @pytest.mark.skip()
    def test_min_stock_is_zero_for_non_unitary(self):
        assert False