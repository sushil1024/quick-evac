from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .zone import Zone
from .user_location import UserLocation