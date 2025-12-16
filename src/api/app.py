# src/api/app.py
"""
Main Flask application for Churn AI
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
from src.config import config


def create_app(config_name='development'):
    """Application factory"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Store predictor on app (will load model later)
    app.predictor = None
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "ok",
            "service": "churn-ai-api",
            "version": "1.0.0",
            "model_loaded": app.predictor is not None
        }), 200
    
    # Test endpoint
    @app.route('/api/v1/test', methods=['GET'])
    def test():
        """Test endpoint"""
        from datetime import datetime
        return jsonify({
            "message": "API is working!",
            "timestamp": str(datetime.now())
        }), 200
    
    # Predict endpoint (placeholder for now)
    @app.route('/api/v1/predict', methods=['POST'])
    def predict():
        """Placeholder prediction endpoint"""
        return jsonify({
            "status": "error",
            "message": "Model not yet loaded. Run model training first."
        }), 503
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)

