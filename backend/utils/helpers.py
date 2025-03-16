import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import all_blueprints

def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): Test configuration
        
    Returns:
        Flask: Configured Flask application
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object('config.Config')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
    
    # Basic route for health check
    @app.route('/health')
    def health_check():
        return {'status': 'ok'}
    
    return app

def format_phone_number(phone_number):
    """
    Format phone number to E.164 format for Twilio.
    
    Args:
        phone_number (str): Phone number in any format
        
    Returns:
        str: Phone number in E.164 format
    """
    # Remove any non-digit characters
    digits_only = ''.join(filter(str.isdigit, phone_number))
    
    # Ensure it has country code (add +1 for US if not present)
    if len(digits_only) == 10:  # US number without country code
        return f"+1{digits_only}"
    elif len(digits_only) > 10:  # Assumes it already has country code
        return f"+{digits_only}"
    else:
        # Invalid phone number, but return it anyway
        return f"+{digits_only}"