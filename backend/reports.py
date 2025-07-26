# reports.py
from flask import Blueprint, request, jsonify
from models import db, Product, OrderItem, InventoryItem
from sqlalchemy import func, desc

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/top-products', methods=['GET'])
def top_products():
    q = (
        db.session.query(
            Product.id,
            Product.name,
            func.count(OrderItem.id).label('sold_count')
        )
        .join(OrderItem, OrderItem.product_id==Product.id)
        .group_by(Product.id)
        .order_by(desc('sold_count'))
        .limit(5)
        .all()
    )
    return jsonify([{'id': p.id, 'name': p.name, 'sold': p.sold_count} for p in q])

@reports_bp.route('/status/<int:product_id>', methods=['GET'])
def product_status(product_id):
    items = OrderItem.query.filter_by(product_id=product_id).all()
    return jsonify([{'order_id': i.order_id, 'status': i.status} for i in items])

@reports_bp.route('/inventory-count', methods=['GET'])
def inventory_count():
    name     = request.args.get('name', '')
    category = request.args.get('category', '')
    cnt = (
        db.session.query(func.count(InventoryItem.id))
        .filter(InventoryItem.product_name.ilike(f"%{name}%"))
        .filter(InventoryItem.product_category==category)
        .filter(InventoryItem.sold_at.is_(None))
        .scalar()
    )
    return jsonify({'available': cnt})
