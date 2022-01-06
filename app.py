from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)

from products import products

# Testing Route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# Testing Route
@app.route('/', methods=['GET'])
def home():
    return '<h1>Hola Mundo!!!</h1>'

# Get Data Routes
@app.route('/products')
def getProducts():
    conexion=sqlite3.connect("data.sqlite")
    cursor=conexion.execute("select * from notes")
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()

    json_data=[]
    for result in rv:
        dict_from_list = dict(zip(row_headers, result))
        json_data.append(dict_from_list)

    a = json.dumps(json_data)
    conexion.close()
    # return jsonify(products)
    #return jsonify({'products': a})
    return a


@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [
        product for product in products if product['name'] == product_name.lower()]
    if (len(productsFound) > 0):
        return jsonify({'product': productsFound[0]})
    return jsonify({'message': 'Product Not found'})

# Create Data Routes
@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': 10
    }
    products.append(new_product)
    return jsonify({'products': products})

# Update Data Route
@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound) > 0):
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            'message': 'Product Updated',
            'product': productsFound[0]
        })
    return jsonify({'message': 'Product Not found'})

# DELETE Data Route
@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            'message': 'Product Deleted',
            'products': products
        })

if __name__ == '__main__':
    app.run(debug=True, port=4000)
