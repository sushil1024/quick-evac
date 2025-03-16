from flask import request, jsonify, current_app
from backend.routes import location_bp
from backend.models import db, UserLocation
from backend.services.location_service import LocationService
from backend.services.zone_service import ZoneService
from backend.services.sms_service import SMSService

# Initialize services
location_service = LocationService()
zone_service = ZoneService()
sms_service = SMSService()

@location_bp.route('/check', methods=['POST'])
def check_location():
    """
    Check if user's location is in a danger zone and send SMS if needed.
    
    Request body:
        {
            "phone_number": "1234567890",
            "latitude": 37.7749,
            "longitude": -122.4194
        }
    
    Returns:
        JSON response with location information and evacuation details if applicable
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['phone_number', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        phone_number = data['phone_number']
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        
        # Get address from coordinates
        address = location_service.get_address_from_coordinates(latitude, longitude)

        print("User location: ", latitude, longitude, address)
        print("Address: ", address)
        
        # Check if user is in a danger zone
        in_zone, zone = zone_service.is_in_zone(latitude, longitude)
        
        # Prepare response data
        response_data = {
            'success': True,
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'address': address
            },
            'in_danger_zone': in_zone
        }
        
        if in_zone and zone:
            # User is in a zone, add zone information to response
            response_data['zone'] = zone.to_dict()
            
            # If it's a RED or ORANGE zone, find the nearest safe zone and get directions
            if zone.type in ['RED', 'ORANGE']:
                nearest_safe_zone, distance = zone_service.find_nearest_safe_zone(latitude, longitude)
                
                if nearest_safe_zone:
                    # Get directions to the safe zone
                    directions = location_service.get_directions(
                        latitude, longitude, 
                        nearest_safe_zone.latitude, nearest_safe_zone.longitude
                    )
                    
                    if directions:
                        response_data['evacuation'] = {
                            'safe_zone': nearest_safe_zone.to_dict(),
                            'distance': distance,
                            'directions': directions
                        }
                    
                    print("Sending SMS alert...")
                    print("Phone number:", phone_number)
                    print("Zone type:", zone.type)
                    print("Current address:", address)
                    print("Directions:", directions)
                    
                    # Send SMS alert based on zone type
                    # sms_service.send_evacuation_alert(
                    #     phone_number, 
                    #     zone.type, 
                    #     address, 
                    #     directions
                    # )
            elif zone.type == 'GREEN':
                print("Green zone, no evacuation needed...")
                print("Phone number:", phone_number)
                print("Zone type:", zone.type)
                print("Current address:", address)


                # # Send a safety notification for green zones
                # sms_service.send_evacuation_alert(phone_number, zone.type, address)
        
        # Save user location to database
        user_location = location_service.save_user_location(
            phone_number=phone_number,
            latitude=latitude,
            longitude=longitude,
            address=address,
            in_danger_zone=in_zone,
            zone_id=zone.id if in_zone and zone else None
        )
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error checking location: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500