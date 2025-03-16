import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the application."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_for_development')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///quick_evac.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google Maps API configuration
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Twilio configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Zone types
    ZONE_TYPES = {
        'RED': 'High Danger',
        'ORANGE': 'Medium Danger',
        'GREEN': 'Safe'
    }