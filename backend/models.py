# models.py
from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = 'user'
    id             = db.Column(db.Integer, primary_key=True)
    first_name     = db.Column(db.String, nullable=False)
    last_name      = db.Column(db.String, nullable=False)
    email          = db.Column(db.String, unique=True, nullable=False)
    password       = db.Column(db.String, nullable=False)
    age            = db.Column(db.Integer)
    gender         = db.Column(db.String)
    state          = db.Column(db.String)
    street_address = db.Column(db.String)
    postal_code    = db.Column(db.String)
    city           = db.Column(db.String)
    country        = db.Column(db.String)
    latitude       = db.Column(db.Float)
    longitude      = db.Column(db.Float)
    traffic_source = db.Column(db.String)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    sessions       = db.relationship('ConversationSession', back_populates='user')


class DistributionCentre(db.Model):
    __tablename__ = 'distribution_centres'
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String, nullable=False)
    latitude  = db.Column(db.Float)
    longitude = db.Column(db.Float)


class Product(db.Model):
    __tablename__ = 'products'
    id                      = db.Column(db.Integer, primary_key=True)
    cost                    = db.Column(db.Float)
    category                = db.Column(db.String)
    name                    = db.Column(db.String)
    brand                   = db.Column(db.String)
    retail_price            = db.Column(db.Float)
    department              = db.Column(db.String)
    sku                     = db.Column(db.String)
    distribution_center_id  = db.Column(db.Integer, db.ForeignKey('distribution_centres.id'))
    distribution_centre     = db.relationship('DistributionCentre', backref='products')


class Order(db.Model):
    __tablename__ = 'orders'
    order_id     = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'))
    status       = db.Column(db.String)
    gender       = db.Column(db.String)
    created_at   = db.Column(db.DateTime)
    returned_at  = db.Column(db.DateTime)
    shipped_at   = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    num_of_item  = db.Column(db.Integer)
    user         = db.relationship('User', backref='orders')


class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    id                             = db.Column(db.Integer, primary_key=True)
    product_id                     = db.Column(db.Integer, db.ForeignKey('products.id'))
    created_at                     = db.Column(db.DateTime)
    sold_at                        = db.Column(db.DateTime)
    cost                           = db.Column(db.Float)
    product_category               = db.Column(db.String)
    product_name                   = db.Column(db.String)
    product_brand                  = db.Column(db.String)
    product_retail_price           = db.Column(db.Float)
    product_department             = db.Column(db.String)
    product_sku                    = db.Column(db.String)
    product_distribution_center_id = db.Column(db.Integer, db.ForeignKey('distribution_centres.id'))
    product                        = db.relationship('Product')


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id                = db.Column(db.Integer, primary_key=True)
    order_id          = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    user_id           = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id        = db.Column(db.Integer, db.ForeignKey('products.id'))
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'))
    status            = db.Column(db.String)
    created_at        = db.Column(db.DateTime)
    shipped_at        = db.Column(db.DateTime)
    delivered_at      = db.Column(db.DateTime)
    returned_at       = db.Column(db.DateTime)
    sale_price        = db.Column(db.Float)
    order             = db.relationship('Order', backref='items')
    product           = db.relationship('Product')
    user              = db.relationship('User')


class ConversationSession(db.Model):
    __tablename__ = 'conversation_sessions'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    user         = db.relationship('User', back_populates='sessions')
    chats        = db.relationship('Chat', back_populates='session', cascade='delete')


class Chat(db.Model):
    __tablename__ = 'chats'
    id         = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('conversation_sessions.id'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    response   = db.Column(db.Text, nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    session    = db.relationship('ConversationSession', back_populates='chats')
    user       = db.relationship('User')
