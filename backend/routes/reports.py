from flask import Blueprint, jsonify
from models.product import Product
from models.order import Order

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route("/products", methods=["GET"])
def get_products():
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in Product.query.all()])

@reports_bp.route("/orders", methods=["GET"])
def get_orders():
    return jsonify([{"id": o.id, "customer": o.customer_name, "quantity": o.quantity} for o in Order.query.all()])
