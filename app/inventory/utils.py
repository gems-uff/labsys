def stock_is_at_minimum(catalog_product):
    if catalog_product.count_amount_stock_products(
    ) <= catalog_product.min_stock:
        return True
    return False
