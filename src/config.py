import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    CORS_HEADERS = 'Content-Type'
    
    # Add other configuration variables as needed
    MAX_PARTICIPANTS = 1000
    MIN_PARTICIPANTS = 1 