# src/config.py
"""
Configuration for Churn AI
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # API Keys
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_")
    INTERCOM_TOKEN = os.getenv("INTERCOM_TOKEN", "")
    
    # Flask settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///churn.db")
    
    # Model paths
    MODEL_PATH = "models/churn_model.pkl"
    SCALER_PATH = "models/scaler.pkl"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

