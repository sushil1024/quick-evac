from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from backend.models.zone import Zone
from backend.models.user_location import UserLocation