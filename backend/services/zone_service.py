from flask import current_app
from models import db, Zone
from .location_service import LocationService

class ZoneService:
    """Service for handling zone-related operations."""
    
    def __init__(self):
        """Initialize the location service."""
        self.location_service = LocationService()
    
    def get_all_zones(self):
        """
        Get all zones from the database.
        
        Returns:
            list: List of all zone objects
        """
        return Zone.query.all()
    
    def get_zone_by_id(self, zone_id):
        """
        Get zone by ID.
        
        Args:
            zone_id (int): Zone ID
            
        Returns:
            Zone: Zone object or None if not found
        """
        return Zone.query.get(zone_id)
    
    def get_zones_by_type(self, zone_type):
        """
        Get zones by type.
        
        Args:
            zone_type (str): Zone type (RED, ORANGE, GREEN)
            
        Returns:
            list: List of zone objects matching the type
        """
        return Zone.query.filter_by(type=zone_type).all()
    
    def create_zone(self, name, zone_type, latitude, longitude, radius, description=None):
        """
        Create a new zone.
        
        Args:
            name (str): Zone name
            zone_type (str): Zone type (RED, ORANGE, GREEN)
            latitude (float): Zone center latitude
            longitude (float): Zone center longitude
            radius (float): Zone radius in kilometers
            description (str, optional): Zone description
            
        Returns:
            Zone: Created zone object
        """
        # Get address from coordinates
        address = self.location_service.get_address_from_coordinates(latitude, longitude)
        
        zone = Zone(
            name=name,
            type=zone_type,
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            address=address,
            description=description
        )
        
        db.session.add(zone)
        db.session.commit()
        
        return zone
    
    def update_zone(self, zone_id, **kwargs):
        """
        Update an existing zone.
        
        Args:
            zone_id (int): Zone ID
            **kwargs: Fields to update
            
        Returns:
            Zone: Updated zone object or None if not found
        """
        zone = self.get_zone_by_id(zone_id)
        if not zone:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(zone, key):
                setattr(zone, key, value)
        
        # If coordinates were updated, update the address
        if 'latitude' in kwargs or 'longitude' in kwargs:
            zone.address = self.location_service.get_address_from_coordinates(
                zone.latitude, zone.longitude
            )
        
        db.session.commit()
        
        return zone
    
    def delete_zone(self, zone_id):
        """
        Delete a zone.
        
        Args:
            zone_id (int): Zone ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        zone = self.get_zone_by_id(zone_id)
        if not zone:
            return False
        
        db.session.delete(zone)
        db.session.commit()
        
        return True
    
    def is_in_zone(self, latitude, longitude, zone_id=None):
        """
        Check if coordinates are in a specific zone or any zone.
        
        Args:
            latitude (float): Latitude to check
            longitude (float): Longitude to check
            zone_id (int, optional): Specific zone ID to check
            
        Returns:
            tuple: (bool, Zone) - Whether in zone and the zone object
        """
        if zone_id:
            # Check specific zone
            zone = self.get_zone_by_id(zone_id)
            if not zone:
                return False, None
                
            distance = self.location_service.calculate_distance(
                latitude, longitude, zone.latitude, zone.longitude
            )
            
            if distance <= zone.radius:
                return True, zone
            
            return False, None
        else:
            # Check all zones, prioritizing red zones
            zones = self.get_all_zones()
            
            # Sort by zone type priority (RED > ORANGE > GREEN)
            priority = {'RED': 0, 'ORANGE': 1, 'GREEN': 2}
            zones.sort(key=lambda z: priority.get(z.type, 3))
            
            for zone in zones:
                distance = self.location_service.calculate_distance(
                    latitude, longitude, zone.latitude, zone.longitude
                )
                
                if distance <= zone.radius:
                    return True, zone
            
            return False, None
    
    def find_nearest_safe_zone(self, latitude, longitude):
        """
        Find the nearest GREEN (safe) zone from the given coordinates.
        
        Args:
            latitude (float): Current latitude
            longitude (float): Current longitude
            
        Returns:
            tuple: (Zone, float) - Nearest safe zone and distance in km
        """
        safe_zones = self.get_zones_by_type('GREEN')
        
        if not safe_zones:
            return None, None
        
        nearest_zone = None
        min_distance = float('inf')
        
        for zone in safe_zones:
            distance = self.location_service.calculate_distance(
                latitude, longitude, zone.latitude, zone.longitude
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_zone = zone
        
        return nearest_zone, min_distance