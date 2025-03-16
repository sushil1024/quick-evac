from backend.models import db
from datetime import datetime

class UserLocation(db.Model):
    """
    Model for storing user location data.
    
    Attributes:
        id (int): Primary key
        phone_number (str): User's phone number
        latitude (float): User's latitude
        longitude (float): User's longitude
        address (str): User's address determined from coordinates
        in_danger_zone (bool): Whether user is in a danger zone
        zone_id (int): Foreign key to the zone if user is in one
        created_at (datetime): When the record was created
    """
    
    __tablename__ = 'user_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    in_danger_zone = db.Column(db.Boolean, default=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    zone = db.relationship('Zone', backref=db.backref('user_locations', lazy=True))
    
    def __repr__(self):
        return f"<UserLocation {self.phone_number} at ({self.latitude}, {self.longitude})>"
    
    def to_dict(self):
        """Convert user location object to dictionary."""
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'in_danger_zone': self.in_danger_zone,
            'zone_id': self.zone_id,
            'zone_type': self.zone.type if self.zone else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }