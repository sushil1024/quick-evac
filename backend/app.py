"""
Direct entry point for the Quick Evac application. 
This bypasses the need for complex imports and application context management.
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure the app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '1') == '1'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quick_evac.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLE_MAPS_API_KEY'] = os.environ.get('GOOGLE_MAPS_API_KEY')
app.config['TWILIO_ACCOUNT_SID'] = os.environ.get('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN')
app.config['TWILIO_PHONE_NUMBER'] = os.environ.get('TWILIO_PHONE_NUMBER')

# Enable CORS
CORS(app)

# Import and initialize database after app is created
from backend.models import db
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Import and register blueprints
from backend.routes import all_blueprints
for blueprint in all_blueprints:
    app.register_blueprint(blueprint)

# Add health check route
@app.route('/health')
def health_check():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')