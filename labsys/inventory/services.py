from labsys.inventory import models as m

from ..extensions import db


def create_add_transaction_from_order(order, stock):
    user = order.user
    for order_item in order.items:
        product = order_item.item.product
        lot_number = order_item.lot_number
        total_units = order_item.amount * order_item.item.units
        expiration_date = order_item.expiration_date
        transaction = m.Transaction(
            user=user,
            product=product,
            lot_number=lot_number,
            amount=total_units,
            stock=stock,
            category=m.ADD,
            expiration_date=expiration_date,
            order_item=order_item,
        )
        db.session.add(transaction)
    db.session.commit()


def create_sub_transaction(user, product, lot_number, amount, stock):
    transaction = m.Transaction(
        user=user,
        product=product,
        lot_number=lot_number,
        amount=amount,
        stock=stock,
        category=m.SUB,
    )
    db.session.add(transaction)
    db.session.commit()
