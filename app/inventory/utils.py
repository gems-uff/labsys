def stock_is_at_minimum(stock_product, catalog_product):
    if stock_product.amount < catalog_product.min_stock:
        return True
    return False
