from ariadne import MutationType, QueryType, graphql_sync, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

import products_service as service

SWAGGER_URL = '/products/docs'          # where Swagger UI is served
API_URL = '/static/swagger.json'        # the spec file it reads

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Products microservice"},
)
app.register_blueprint(swaggerui_blueprint)

NOT_FOUND = {"msg": "Product not found"}


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(service.list_products())


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = service.get_product(id)
    if product is None:
        return jsonify(NOT_FOUND), 404
    return jsonify(product)


@app.route('/products', methods=['POST'])
def add_product():
    payload = request.get_json()
    service.add_product(payload["name"], payload["price"])
    return '', 201


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    if service.update_product(id, **request.get_json()) is None:
        return jsonify(NOT_FOUND), 404
    return '', 204


@app.route('/products/<int:id>', methods=['DELETE'])
def remove_product(id):
    if not service.delete_product(id):
        return jsonify(NOT_FOUND), 404
    return '', 204


# ---------------------------------------------------------------------------
# GraphQL. Same service, same data -- one endpoint, and the client picks the
# fields. No status codes here: a missing product is a null in the body.
# ---------------------------------------------------------------------------

type_defs = """
    type Product {
        id: Int!
        name: String!
        price: Float!
    }

    type Query {
        products: [Product!]!
        product(id: Int!): Product
    }

    type Mutation {
        addProduct(name: String!, price: Float!): Product!
        updateProduct(id: Int!, name: String, price: Float): Product
        deleteProduct(id: Int!): Boolean!
    }
"""

query = QueryType()
mutation = MutationType()


@query.field("products")
def resolve_products(*_):
    return service.list_products()


@query.field("product")
def resolve_product(_, info, id):
    return service.get_product(id)


@mutation.field("addProduct")
def resolve_add_product(_, info, name, price):
    return service.add_product(name, price)


@mutation.field("updateProduct")
def resolve_update_product(_, info, id, **fields):
    # Only the arguments the client actually sent arrive in **fields.
    return service.update_product(id, **fields)


@mutation.field("deleteProduct")
def resolve_delete_product(_, info, id):
    return service.delete_product(id)


schema = make_executable_schema(type_defs, query, mutation)
explorer_html = ExplorerGraphiQL().html(None)


@app.route('/graphql', methods=['GET'])
def graphql_explorer():
    return explorer_html, 200


@app.route('/graphql', methods=['POST'])
def graphql_server():
    success, result = graphql_sync(
        schema,
        request.get_json(),
        context_value={"request": request},
        debug=app.debug,
    )
    return jsonify(result), 200 if success else 400
