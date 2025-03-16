from . import db
from datetime import datetime

class Zone(db.Model):
    """
    Model for danger zones.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the zone
        type (str): Type of zone (RED, ORANGE, GREEN)
        latitude (float): Latitude of the zone center
        longitude (float): Longitude of the zone center
        radius (float): Radius of the zone in kilometers
        address (str): Human-readable address of the zone
        description (str): Description of the zone
        created_at (datetime): When the zone was created
        updated_at (datetime): When the zone was last updated
    """
    
    __tablename__ = 'zones'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # RED, ORANGE, GREEN
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)  # radius in kilometers
    address = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Zone {self.name} ({self.type})>"
    
    def to_dict(self):
        """Convert zone object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius': self.radius,
            'address': self.address,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }