"""The products store, independent of how it is exposed."""

_products = {
    1: {"id": 1, "name": "Product 1", "price": 10.99},
    2: {"id": 2, "name": "Product 2", "price": 19.99},
    3: {"id": 3, "name": "Product 3", "price": 5.99},
}


def list_products():
    return list(_products.values())


def get_product(id):
    """The product, or None if there is no such id."""
    return _products.get(id)


def add_product(name, price):
    new_id = max(_products, default=0) + 1
    _products[new_id] = {"id": new_id, "name": name, "price": price}
    return _products[new_id]


def update_product(id, **fields):
    """Merge the given fields into the product; None if there is no such id."""
    product = _products.get(id)
    if product is None:
        return None
    product.update(fields)
    return product


def delete_product(id):
    """True if a product was removed, False if there was nothing to remove."""
    return _products.pop(id, None) is not None
