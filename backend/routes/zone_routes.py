from flask import request, jsonify, current_app
from backend.routes import zone_bp
from backend.models import Zone
from backend.services.zone_service import ZoneService

# Initialize the zone service
zone_service = ZoneService()

@zone_bp.route('/', methods=['GET'])
def get_all_zones():
    """
    Get all zones or filter by type.
    
    Query parameters:
        type (optional): Filter zones by type (RED, ORANGE, GREEN)
    
    Returns:
        JSON array of zones
    """
    try:
        zone_type = request.args.get('type')
        
        if zone_type:
            zones = zone_service.get_zones_by_type(zone_type.upper())
        else:
            zones = zone_service.get_all_zones()
        
        return jsonify({
            'success': True,
            'zones': [zone.to_dict() for zone in zones]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting zones: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching zones'
        }), 500

@zone_bp.route('/<int:zone_id>', methods=['GET'])
def get_zone(zone_id):
    """
    Get a zone by ID.
    
    Parameters:
        zone_id (int): Zone ID
    
    Returns:
        JSON zone object
    """
    try:
        zone = zone_service.get_zone_by_id(zone_id)
        
        if not zone:
            return jsonify({
                'success': False,
                'message': f'Zone with ID {zone_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'zone': zone.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting zone: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching the zone'
        }), 500

@zone_bp.route('/', methods=['POST'])
def create_zone():
    """
    Create a new zone.
    
    Request body:
        {
            "name": "Zone Name",
            "type": "RED", // RED, ORANGE, or GREEN
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius": 1.5, // radius in kilometers
            "description": "Zone description" // optional
        }
    
    Returns:
        JSON created zone object
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'type', 'latitude', 'longitude', 'radius']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Validate zone type
        valid_types = ['RED', 'ORANGE', 'GREEN']
        if data['type'].upper() not in valid_types:
            return jsonify({
                'success': False,
                'message': f'Invalid zone type. Must be one of: {", ".join(valid_types)}'
            }), 400
        
        # Create zone
        zone = zone_service.create_zone(
            name=data['name'],
            zone_type=data['type'].upper(),
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            radius=float(data['radius']),
            description=data.get('description')
        )
        
        return jsonify({
            'success': True,
            'message': 'Zone created successfully',
            'zone': zone.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error creating zone: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while creating the zone'
        }), 500

@zone_bp.route('/<int:zone_id>', methods=['PUT'])
def update_zone(zone_id):
    """
    Update an existing zone.
    
    Parameters:
        zone_id (int): Zone ID
    
    Request body:
        {
            "name": "Updated Zone Name", // optional
            "type": "ORANGE", // optional
            "latitude": 37.7749, // optional
            "longitude": -122.4194, // optional
            "radius": 2.0, // optional
            "description": "Updated description" // optional
        }
    
    Returns:
        JSON updated zone object
    """
    try:
        data = request.get_json()
        
        # Validate zone type if provided
        if 'type' in data:
            valid_types = ['RED', 'ORANGE', 'GREEN']
            if data['type'].upper() not in valid_types:
                return jsonify({
                    'success': False,
                    'message': f'Invalid zone type. Must be one of: {", ".join(valid_types)}'
                }), 400
            data['type'] = data['type'].upper()
        
        # Convert numeric fields to float
        for field in ['latitude', 'longitude', 'radius']:
            if field in data:
                data[field] = float(data[field])
        
        # Update zone
        updated_zone = zone_service.update_zone(zone_id, **data)
        
        if not updated_zone:
            return jsonify({
                'success': False,
                'message': f'Zone with ID {zone_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Zone updated successfully',
            'zone': updated_zone.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error updating zone: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while updating the zone'
        }), 500

@zone_bp.route('/<int:zone_id>', methods=['DELETE'])
def delete_zone(zone_id):
    """
    Delete a zone.
    
    Parameters:
        zone_id (int): Zone ID
    
    Returns:
        JSON success message
    """
    try:
        success = zone_service.delete_zone(zone_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': f'Zone with ID {zone_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Zone deleted successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error deleting zone: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting the zone'
        }), 500