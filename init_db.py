"""
Script to initialize database with sample data.
Run this script after setting up the application to create test zones.
"""

from backend.utils.helpers import create_app
from backend.models import db, Zone
from backend.services.location_service import LocationService

def init_db():
    print("Initializing database with sample data...")
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Initialize services
        location_service = LocationService()
        
        # Create sample zones
        # These coordinates are approximations, replace with actual coordinates for your area
        sample_zones = [
            # Red zones (danger)
            {
                'name': 'Downtown Danger Zone',
                'type': 'RED',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'radius': 1.0,
                'description': 'High risk area due to potential flooding and structural hazards.'
            },
            {
                'name': 'Industrial Hazard Zone',
                'type': 'RED',
                'latitude': 37.7833,
                'longitude': -122.4167,
                'radius': 0.8,
                'description': 'Chemical hazards and industrial risks present.'
            },
            
            # Orange zones (medium risk)
            {
                'name': 'Coastal Warning Zone',
                'type': 'ORANGE',
                'latitude': 37.8083,
                'longitude': -122.4156,
                'radius': 1.2,
                'description': 'Moderate risk of coastal flooding and storm surge.'
            },
            {
                'name': 'Hill District Alert Zone',
                'type': 'ORANGE',
                'latitude': 37.7516,
                'longitude': -122.4477,
                'radius': 0.9,
                'description': 'Landslide risk during heavy rain periods.'
            },
            
            # Green zones (safe)
            {
                'name': 'Central Park Safe Zone',
                'type': 'GREEN',
                'latitude': 37.7694,
                'longitude': -122.4862,
                'radius': 1.5,
                'description': 'Designated evacuation area with emergency supplies and shelter.'
            },
            {
                'name': 'Highland Safe Zone',
                'type': 'GREEN',
                'latitude': 37.7928,
                'longitude': -122.4551,
                'radius': 1.2,
                'description': 'Elevated area safe from flooding with medical facilities.'
            }
        ]
        
        for zone_data in sample_zones:
            # Get address from coordinates
            address = location_service.get_address_from_coordinates(
                zone_data['latitude'], 
                zone_data['longitude']
            )
            
            # Create zone
            zone = Zone(
                name=zone_data['name'],
                type=zone_data['type'],
                latitude=zone_data['latitude'],
                longitude=zone_data['longitude'],
                radius=zone_data['radius'],
                address=address,
                description=zone_data['description']
            )
            
            db.session.add(zone)
        
        # Commit all changes
        db.session.commit()
        
        # Verify zones were created
        zones = Zone.query.all()
        print(f"Created {len(zones)} zones:")
        for zone in zones:
            print(f"  - {zone.name} ({zone.type}): {zone.address}")
            
    print("Database initialization complete!")

if __name__ == "__main__":
    init_db()