from ..extensions import db
from labsys.inventory import models as m


def create_add_transaction_from_order(order, stock):
    user = order.user
    for order_item in order.items:
        product = order_item.item.product
        lot_number = order_item.lot_number
        total_units = order_item.amount * order_item.item.units
        expiration_date = order_item.expiration_date
        transaction = m.Transaction(
            user,
            product,
            lot_number,
            total_units,
            stock,
            m.ADD,
            expiration_date,
        )
        db.session.add(transaction)
    db.session.commit()


def create_sub_transaction(user, product, lot_number, amount, stock):
    try:
        transaction = m.Transaction(
            user,
            product,
            lot_number,
            amount,
            stock,
            m.SUB,
        )
        db.session.add(transaction)
        db.session.commit()
    except ValueError as error:
        print(error)
