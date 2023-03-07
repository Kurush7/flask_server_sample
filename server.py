from flask import Flask, Response, request
from repository import Repository
from templates import *
import json
from qrconfig import QRYamlConfig

app = Flask('amazon',
            static_url_path='',
            static_folder='./static',
            template_folder='./static/templates'
            )

repo = Repository()


@app.route('/')
def home():
    return '<html>this is home</html>'


@app.route('/products')
def get_products():
    products = repo.get_products()
    if products is None:
        return Response(status=500, response='database failed')
    return make_products_page(products)


@app.route('/products/<uuid>', methods=['GET'])
def get_product(uuid):
    product = repo.get_product(uuid)
    if product is None:
        return Response(status=500, response='database failed')
    return make_product_page(product)


@app.route('/products', methods=['POST'])
def create_product():
    data = request.json

    ok = repo.create_product(data)
    if not ok:
        return Response(status=500, response='failed to create product')
    return Response(status=200, response='ok')

@app.route('/products/create')
def create_product_page():
    return make_create_product_page()


@app.route('/manufacturers/', methods=['POST'])
def create_manufacturer():
    data = request.args

    ok = repo.create_manufacturer(data)
    if not ok:
        return Response(status=500, response='failed to create manufacturer')
    return Response(status=200, response='ok')


if __name__ == '__main__':
    config = QRYamlConfig()
    config.read_config()

    host, port = config.server.host, config['server']['port']

    app.run(host=host, port=port, debug=True)