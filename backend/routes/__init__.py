from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Import customer routes
from .customer_routes import *