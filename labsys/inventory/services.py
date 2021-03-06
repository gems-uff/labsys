from ..extensions import db
from labsys.inventory import models as m


def create_add_transactions_from_order(order, stock):
    user = order.user
    for order_item in order.items:
        product = order_item.item.product
        lot_number = order_item.lot_number
        total_units = order_item.amount * order_item.item.units
        transaction = m.Transaction(
            user,
            product,
            lot_number,
            total_units,
            stock,
            m.ADD,
        )
        db.session.add(transaction)
    db.session.commit()


def create_sub_transaction(user, product, lot_number, amount, stock):
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
