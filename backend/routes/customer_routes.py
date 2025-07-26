from flask import Blueprint, request, jsonify
from backend.database.lancedb import get_db_connection
from backend.utils.error_handling import handle_error

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        return jsonify(products), 200
    except Exception as e:
        return handle_error(e)

@customer_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Orders (user_id, status, gender, created_at, num_of_item) VALUES (?, ?, ?, ?, ?)",
                       (order_data['user_id'], order_data['status'], order_data['gender'], order_data['created_at'], order_data['num_of_item']))
        conn.commit()
        return jsonify({"message": "Order created successfully"}), 201
    except Exception as e:
        return handle_error(e)

@customer_bp.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (first_name, last_name, email, age, gender, state, street_address, postal_code, city, country, latitude, longitude, traffic_source, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_data['first_name'], user_data['last_name'], user_data['email'], user_data['age'], user_data['gender'], user_data['state'], user_data['street_address'], user_data['postal_code'], user_data['city'], user_data['country'], user_data['latitude'], user_data['longitude'], user_data['traffic_source'], user_data['created_at']))
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return handle_error(e)