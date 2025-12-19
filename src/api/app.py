# src/api/app.py
"""
Main Flask application for Churn AI
"""

from flask import Flask, jsonify
from flask_cors import CORS
from src.config import config
from src.models.churn_model import ChurnPredictorModel


def create_app(config_name='development'):
    """Application factory"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app)
    
    # Load ML model
    print("🤖 Loading churn prediction model...")
    try:
        predictor = ChurnPredictorModel()
        predictor.load('models/churn_model.pkl')
        app.predictor = predictor
        print("✅ Model loaded successfully")
    except FileNotFoundError:
        print("⚠️ Model not found. Train it first: python3 src/models/churn_model.py")
        app.predictor = None
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        app.predictor = None
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            "status": "ok",
            "service": "churn-ai-api",
            "model_loaded": app.predictor is not None
        }), 200
    
    # Register API routes
    from src.api.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Server error"}), 500
    
    return app


import os

if __name__ == "__main__":
    app = create_app("development")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

