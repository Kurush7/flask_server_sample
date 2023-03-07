from typing import Dict, List
from flask import render_template


def make_product_page(product: Dict):
    return f'''
    <html>
      <head>
        <title>Product page</title>
      </head>
      <body>
        <h1>Product {product['uuid']}</h1>
        <p>uuid = {product['uuid']}</p>
        <p>name = {product['name']}</p>
        <p>price = {product['price']}</p>
        <p>rating = {product['rating']}</p>
        <p>count = {product['count']}</p>
        <p>description = {product['description']}</p>
      </body>
    </html>
    '''


def make_products_page(products: List[Dict]):
    return render_template("products.html",
                           products=products,
                           title='title'
                           )

def make_create_product_page():
    return render_template("create_product.html",
                           url='http://localhost:5000'
                           )
