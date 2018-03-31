import os, unittest, datetime
from flask import url_for, request

from labsys.app import create_app, db
from labsys.auth.models import Role, User
import labsys.inventory.models as models


class TestInventoryViews(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        db.create_all()
        db.session.add(models.Stock(name='Test Stock'))
        db.session.commit()
        Role.insert_roles()
        staff = Role.query.filter_by(name='Staff').first()
        self.user = User(email='user@example.com', password='example', role=staff, confirmed=True)
        self.user.role = Role.query.filter_by(name='Staff').first()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_purchase_same_product_two_catalogs_same_lot(self):
        spec1 = models.Specification('cat1', 'man1', units=1)
        db.session.add(spec1)
        spec2 = models.Specification('cat2', 'man1', units=10)
        db.session.add(spec2)
        product1 = models.Product('Product1', spec1)
        product1.specifications.append(spec2)
        db.session.add(product1)
        db.session.commit()
        with self.client as client:
            # login
            res = client.post(url_for('auth.login'), data={
                'email': 'user@example.com',
                'password': 'example',
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Go to purchase screen
            res = client.get(url_for('inventory.purchase_product'),
                             follow_redirects=False)
            self.assertEqual(res.status_code, 200)
            data = res.get_data(as_text=True)
            self.assertEqual('/inventory/orders/add', request.path)

            # Add order_item to cart
            order_item_dict = {
                'item_id': spec1.id,
                'amount': 5,
                'lot_number': 'lot1',
                'expiration_date': '2018-03-21',
            }
            res = client.post(url_for('inventory.purchase_product'),
                                      data=order_item_dict,
                                      follow_redirects=True)
            self.assertIn('adicionado ao carrinho', res.get_data(as_text=True))

            # Add another order_item to cart same lot
            order_item_dict = {
                'item_id': spec2.id,
                'amount': 5,
                'lot_number': 'lot1',
                'expiration_date': '2018-03-21',
            }
            res = client.post(url_for('inventory.purchase_product'),
                                      data=order_item_dict,
                                      follow_redirects=True)
            self.assertIn('adicionado ao carrinho', res.get_data(as_text=True))

            # Go to checkout
            res = client.post(url_for('inventory.purchase_product'),
                                       data={'finish_order': True},
                                       follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertEqual('/inventory/orders/checkout', request.path)

            # Finish order
            order_dict = {
                'invoice_type': 'Nota Fiscal',
                'invoice': 'test invoice',
                'financier': 'test financier',
                'notes': 'test notes',
            }
            client.post(url_for('inventory.checkout'),
                        data=order_dict,
                        follow_redirects=True)
            # Assert 2 transactions were created
            transactions = models.Transaction.query.all()
            self.assertEqual(len(transactions), 2)
            transaction1 = transactions[0]

            # Assert user was correctly assigned
            self.assertEqual(transaction1.user, self.user)
            order = models.Order.query.first()
            self.assertEqual(order.user, self.user)

            # Assert only 1 stock_product was created (same lot)
            stock_products = models.StockProduct.query.all()
            self.assertEqual(len(stock_products), 1)

            # Assert products were added to stock
            stock = models.Stock.get_reactive_stock()
            self.assertEqual(stock_products, stock.stock_products)

            # Assert its amount is 5 + 50
            stock_product = stock_products[0]
            self.assertEqual(stock_product.amount, 55)

    def test_purchase_same_product_two_catalogs_diff_lot(self):
        spec1 = models.Specification('cat1', 'man1', units=1)
        db.session.add(spec1)
        spec2 = models.Specification('cat2', 'man1', units=10)
        db.session.add(spec2)
        product1 = models.Product('Product1', spec1)
        product1.specifications.append(spec2)
        db.session.add(product1)
        db.session.commit()
        with self.client as client:
            # login
            res = client.post(url_for('auth.login'), data={
                'email': 'user@example.com',
                'password': 'example',
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Go to purchase screen
            res = client.get(url_for('inventory.purchase_product'),
                             follow_redirects=False)
            self.assertEqual(res.status_code, 200)
            data = res.get_data(as_text=True)
            self.assertEqual('/inventory/orders/add', request.path)

            # Add order_item to cart
            order_item_dict = {
                'item_id': spec1.id,
                'amount': 5,
                'lot_number': 'lot1',
                'expiration_date': '2018-03-21',
            }
            res = client.post(url_for('inventory.purchase_product'),
                                      data=order_item_dict,
                                      follow_redirects=True)
            self.assertIn('adicionado ao carrinho', res.get_data(as_text=True))

            # Add another order_item to cart same lot
            order_item_dict = {
                'item_id': spec2.id,
                'amount': 5,
                'lot_number': 'lot2',
                'expiration_date': '2018-03-21',
            }
            res = client.post(url_for('inventory.purchase_product'),
                                      data=order_item_dict,
                                      follow_redirects=True)
            self.assertIn('adicionado ao carrinho', res.get_data(as_text=True))

            # Go to checkout
            res = client.post(url_for('inventory.purchase_product'),
                                       data={'finish_order': True},
                                       follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertEqual('/inventory/orders/checkout', request.path)

            # Finish order
            order_dict = {
                'invoice_type': 'Nota Fiscal',
                'invoice': 'test invoice',
                'financier': 'test financier',
                'notes': 'test notes',
            }
            client.post(url_for('inventory.checkout'),
                        data=order_dict,
                        follow_redirects=True)
            # Assert 2 transactions were created
            transactions = models.Transaction.query.all()
            self.assertEqual(len(transactions), 2)
            transaction1 = transactions[0]

            # Assert user was correctly assigned
            self.assertEqual(transaction1.user, self.user)
            order = models.Order.query.first()
            self.assertEqual(order.user, self.user)

            # Assert 2 stock_products were created (same lot)
            stock_products = models.StockProduct.query.all()
            self.assertEqual(len(stock_products), 2)

            # Assert their amounts are 5 AND 50
            stock_product = stock_products[0]
            self.assertEqual(stock_product.amount, 5)
            stock_product = stock_products[1]
            self.assertEqual(stock_product.amount, 50)

    def test_purchase_2_diff_products(self):
        spec1 = models.Specification('cat1', 'man1', units=1)
        db.session.add(spec1)
        spec2 = models.Specification('cat2', 'man1', units=10)
        db.session.add(spec2)
        product1 = models.Product('Product1', spec1)
        product2 = models.Product('Product2', spec2)
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()
        with self.client as client:
            # login
            res = client.post(url_for('auth.login'), data={
                'email': 'user@example.com',
                'password': 'example',
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Go to purchase screen
            res = client.get(url_for('inventory.purchase_product'),
                             follow_redirects=False)
            self.assertEqual(res.status_code, 200)
            data = res.get_data(as_text=True)
            self.assertEqual('/inventory/orders/add', request.path)

            # Add order_item to cart
            order_item_dict = {
                'item_id': spec1.id,
                'amount': 5,
                'lot_number': 'lot1',
                'expiration_date': '2018-03-21',
            }
            res = client.post(url_for('inventory.purchase_product'),
                                      data=order_item_dict,
                                      follow_redirects=True)
            self.assertIn('adicionado ao carrinho', res.get_data(as_text=True))

            # Add another order_item to cart same lot
            order_item_dict = {
                'item_id': spec2.id,
                'amount': 5,
                'lot_number': 'lot2',
                'expiration_date': '2018-03-21',
            }
            res = client.post(url_for('inventory.purchase_product'),
                                      data=order_item_dict,
                                      follow_redirects=True)
            self.assertIn('adicionado ao carrinho', res.get_data(as_text=True))

            # Go to checkout
            res = client.post(url_for('inventory.purchase_product'),
                                       data={'finish_order': True},
                                       follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertEqual('/inventory/orders/checkout', request.path)

            # Finish order
            order_dict = {
                'invoice_type': 'Nota Fiscal',
                'invoice': 'test invoice',
                'financier': 'test financier',
                'notes': 'test notes',
            }
            client.post(url_for('inventory.checkout'),
                        data=order_dict,
                        follow_redirects=True)
            # Assert 2 transactions were created
            transactions = models.Transaction.query.all()
            self.assertEqual(len(transactions), 2)
            transaction1 = transactions[0]

            # Assert user was correctly assigned
            self.assertEqual(transaction1.user, self.user)
            order = models.Order.query.first()
            self.assertEqual(order.user, self.user)
            self.assertEqual(order.notes, 'test notes')

            # Assert 2 stock_products were created (same lot)
            stock_products = models.StockProduct.query.all()
            self.assertEqual(len(stock_products), 2)

            # Assert their amounts are 5 AND 50
            stock_product = stock_products[0]
            self.assertEqual(stock_product.amount, 5)
            stock_product = stock_products[1]
            self.assertEqual(stock_product.amount, 50)

            # Assert there are 2 products
            self.assertEqual(len(models.Product.query.all()), 2)

    def test_consume_product(self):
        spec1 = models.Specification('cat1', 'man1')
        prod1 = models.Product('Prod1', spec1)
        # Add product to stock
        models.Stock.get_reactive_stock().add(prod1, 'lot1', '2018-03-30', 10)
        stock_products = models.StockProduct.query.all()
        # Asserts they were added
        self.assertEqual(len(stock_products), 1)
        self.assertEqual(stock_products[0].amount, 10)
        with self.client as client:
            # login
            res = client.post(url_for('auth.login'), data={
                'email': 'user@example.com',
                'password': 'example',
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Try to consume amount greater than available
            greater_amount_data={
                'stock_product_id': stock_products[0].id,
                'amount': 11
            }
            res = client.post(url_for('inventory.consume_product'),
                        data=greater_amount_data,
                        follow_redirects=True)
            self.assertIn('Não há o suficiente', res.get_data(as_text=True))
            # Assert stock is intact
            self.assertEqual(stock_products[0].amount, 10)

            # Try to consume a sufficient amount
            sufficient_amount_data={
                'stock_product_id': stock_products[0].id,
                'amount': 9
            }
            res = client.post(url_for('inventory.consume_product'),
                        data=sufficient_amount_data,
                        follow_redirects=True)
            self.assertIn('removidas do estoque', res.get_data(as_text=True))
            # Assert stock was subtracted
            self.assertEqual(stock_products[0].amount, 1)
            # Assert transaction was created
            transactions = models.Transaction.query.all()
            self.assertEqual(len(transactions), 1)
            self.assertEqual(transactions[0].amount, 9)