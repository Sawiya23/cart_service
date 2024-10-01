from flask import Flask, jsonify, request
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulated in-memory cart storage for users
cart = {}

# Fetch the Product Service URL from environment variables
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:5000/products')

# Get the cart for a specific user
@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    user_cart = cart.get(user_id)
    if not user_cart:
        return jsonify({'message': 'Cart is empty'}), 200
    return jsonify(user_cart)

# Add a product to the cart for a specific user
@app.route('/cart/<user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)
    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        product_response.raise_for_status()  # Handle non-200 responses
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Error fetching product', 'error': str(e)}), 500

    product = product_response.json()

    if user_id not in cart:
        cart[user_id] = {}

    if product['name'] in cart[user_id]:
        cart[user_id][product['name']]['quantity'] += quantity
    else:
        cart[user_id][product['name']] = {'price': product['price'], 'quantity': quantity}

    return jsonify(cart[user_id]), 201

# Remove a product from the cart for a specific user
@app.route('/cart/<user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)
    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        product_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Error fetching product', 'error': str(e)}), 500

    product = product_response.json()

    if user_id not in cart or product['name'] not in cart[user_id]:
        return jsonify({'message': 'Product not in cart'}), 404

    cart[user_id][product['name']]['quantity'] -= quantity
    if cart[user_id][product['name']]['quantity'] <= 0:
        del cart[user_id][product['name']]

    return jsonify(cart[user_id]), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
