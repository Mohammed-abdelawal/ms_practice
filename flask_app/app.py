from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/products/docs'          # where Swagger UI is served
API_URL = '/static/swagger.json'        # the spec file it reads

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Products microservice"},
)
app.register_blueprint(swaggerui_blueprint)

products = {
    1: {"id": 1, "name": "Product 1", "price": 10.99},
    2: {"id": 2, "name": "Product 2", "price": 19.99},
    3: {"id": 3, "name": "Product 3", "price": 5.99},
}


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(list(products.values()))


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = products.get(id)
    if product:
        return jsonify(product)
    return jsonify({"msg": "Product not found"}), 404


@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    new_product["id"] = max(products.keys()) + 1
    products[new_product["id"]] = new_product
    return '', 201


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    updated_product = request.get_json()
    product = products.get(id)
    if product:
        for key, value in updated_product.items():
            product[key] = value
        return '', 204
    return jsonify({"msg": "Product not found"}), 404


@app.route('/products/<int:id>', methods=['DELETE'])
def remove_product(id):
    product = products.get(id)
    if product:
        del products[id]
        return '', 204
    return jsonify({"msg": "Product not found"}), 404
