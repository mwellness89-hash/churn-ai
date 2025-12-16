# src/api/routes.py
"""
API Routes for Churn AI
"""

from flask import Blueprint, request, jsonify, current_app
import pandas as pd

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/predict', methods=['POST'])
def predict_churn():
    """
    Predict churn for a single customer
    
    Expected JSON:
    {
      "customer_id": "cus_123",
      "account_age_days": 365,
      "monthly_charges": 99.99,
      ...other features...
    }
    """
    
    try:
        data = request.get_json()
        
        # Required fields
        required = [
            'customer_id', 'account_age_days', 'monthly_charges', 'total_charges',
            'high_bill', 'has_long_contract', 'has_month_to_month', 'num_services',
            'days_inactive', 'is_inactive', 'support_tickets', 'has_support_issues',
            'engagement_score'
        ]
        
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing: {missing}"}), 400
        
        # Create feature dataframe
        features = {
            'account_age_days': float(data['account_age_days']),
            'account_age_months': float(data['account_age_days']) / 30,
            'monthly_charges': float(data['monthly_charges']),
            'total_charges': float(data['total_charges']),
            'high_bill': int(data['high_bill']),
            'has_long_contract': int(data['has_long_contract']),
            'has_month_to_month': int(data['has_month_to_month']),
            'num_services': int(data['num_services']),
            'days_inactive': int(data['days_inactive']),
            'is_inactive': int(data['is_inactive']),
            'support_tickets': int(data['support_tickets']),
            'has_support_issues': int(data['has_support_issues']),
            'engagement_score': float(data['engagement_score'])
        }
        
        X = pd.DataFrame([features])
        
        # Get predictor from app
        predictor = current_app.predictor
        
        if predictor is None:
            return jsonify({"error": "Model not loaded"}), 503
        
        # Predict
        predictions = predictor.predict(X)
        churn_prob = float(predictions['churn_probability'])
        risk = predictions['risk_level']
        
        # Recommend action
        if risk == 'high':
            action = "🚨 URGENT: Schedule CS call + offer 20% discount"
        elif risk == 'medium':
            action = "📧 Send personalized email with feature demo + 10% discount"
        else:
            action = "✅ Continue normal nurture sequence"
        
        return jsonify({
            "customer_id": data['customer_id'],
            "churn_probability": churn_prob,
            "risk_level": risk,
            "recommended_action": action
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    
    predictor = current_app.predictor
    
    if predictor is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    return jsonify({
        "model_type": "XGBoost",
        "version": "1.0",
        "num_features": len(predictor.feature_names),
        "features": predictor.feature_names,
        "accuracy": "84.4%"
    }), 200

