import googlemaps
from math import radians, cos, sin, asin, sqrt
from flask import current_app
from backend.models import db, UserLocation

class LocationService:
    """Service for handling location-related operations."""
    
    def __init__(self):
        """Initialize the service without directly accessing config."""
        self.gmaps = None
    
    def _ensure_gmaps_client(self):
        """Ensure Google Maps client is initialized when needed."""
        if self.gmaps is None:
            self.gmaps = googlemaps.Client(key=current_app.config['GOOGLE_MAPS_API_KEY'])
    
    def get_address_from_coordinates(self, latitude, longitude):
        """
        Get formatted address from coordinates using Google Maps API.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            str: Formatted address or None if not found
        """
        try:
            self._ensure_gmaps_client()
            reverse_geocode_result = self.gmaps.reverse_geocode((latitude, longitude))
            if reverse_geocode_result:
                return reverse_geocode_result[0]['formatted_address']
            return None
        except Exception as e:
            current_app.logger.error(f"Error getting address: {str(e)}")
            return None
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees).
        
        Args:
            lat1, lon1: Coordinates of point 1
            lat2, lon2: Coordinates of point 2
            
        Returns:
            float: Distance in kilometers
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def get_directions(self, origin_lat, origin_lng, destination_lat, destination_lng):
        """
        Get directions from origin to destination using Google Maps API.
        
        Args:
            origin_lat (float): Origin latitude
            origin_lng (float): Origin longitude
            destination_lat (float): Destination latitude
            destination_lng (float): Destination longitude
            
        Returns:
            dict: Directions information
        """
        try:
            self._ensure_gmaps_client()
            directions_result = self.gmaps.directions(
                origin=f"{origin_lat},{origin_lng}",
                destination=f"{destination_lat},{destination_lng}",
                mode="driving"
            )
            
            if directions_result:
                # Extract relevant information from the directions result
                route = directions_result[0]
                legs = route['legs'][0]
                
                return {
                    'distance': legs['distance']['text'],
                    'duration': legs['duration']['text'],
                    'start_address': legs['start_address'],
                    'end_address': legs['end_address'],
                    'steps': [
                        {
                            'instruction': step['html_instructions'],
                            'distance': step['distance']['text'],
                            'duration': step['duration']['text']
                        }
                        for step in legs['steps']
                    ]
                }
            
            return None
        except Exception as e:
            current_app.logger.error(f"Error getting directions: {str(e)}")
            return None
    
    def save_user_location(self, phone_number, latitude, longitude, address, in_danger_zone=False, zone_id=None):
        """
        Save user location to database.
        
        Args:
            phone_number (str): User's phone number
            latitude (float): User's latitude
            longitude (float): User's longitude
            address (str): User's address
            in_danger_zone (bool): Whether user is in a danger zone
            zone_id (int): ID of the zone if user is in one
            
        Returns:
            UserLocation: Saved user location object
        """
        user_location = UserLocation(
            phone_number=phone_number,
            latitude=latitude,
            longitude=longitude,
            address=address,
            in_danger_zone=in_danger_zone,
            zone_id=zone_id
        )
        
        db.session.add(user_location)
        db.session.commit()
        
        return user_location