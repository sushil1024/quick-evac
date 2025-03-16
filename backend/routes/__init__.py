from flask import Blueprint

# Create blueprints
location_bp = Blueprint('location', __name__, url_prefix='/api/location')
zone_bp = Blueprint('zone', __name__, url_prefix='/api/zone')

# Import routes after blueprints are created to avoid circular imports
from backend.routes.location_routes import *
from backend.routes.zone_routes import *

# List of all blueprints
all_blueprints = [location_bp, zone_bp]