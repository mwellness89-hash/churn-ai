# src/models/churn_model.py
"""
Train XGBoost churn prediction model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import xgboost as xgb
import pickle
import os
from src.models.features import FeatureEngineer


class ChurnPredictorModel:
    """Train and save churn prediction model"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def train(self, X, y):
        """Train XGBoost model"""
        
        print("📊 Preparing data...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
        
        # Scale features
        print("📊 Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("🤖 Training XGBoost...")
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='binary:logistic',
            random_state=42,
            scale_pos_weight=2.0,
            n_jobs=-1,
            verbose=0
        )
        
        self.model.fit(X_train_scaled, y_train, eval_set=[(X_test_scaled, y_test)], verbose=False)
        
        # Evaluate
        print("\n📈 Model Performance:")
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        print(f"  AUC Score: {auc:.3f}")
        
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        print(f"  TP: {tp} | TN: {tn} | FP: {fp} | FN: {fn}")
        
        return auc
    
    def predict(self, X):
        """Predict churn probability"""
        
        if self.model is None:
            raise ValueError("Model not trained")
        
        X_scaled = self.scaler.transform(X)
        proba = self.model.predict_proba(X_scaled)[:, 1]
        
        return {
            'churn_probability': (proba * 100).round(1),
            'risk_level': ['high' if p > 0.67 else 'medium' if p > 0.33 else 'low' for p in proba]
        }
    
    def save(self, path='models/churn_model.pkl'):
        """Save model to disk"""
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }, f)
        
        print(f"✅ Model saved to {path}")
    
    def load(self, path='models/churn_model.pkl'):
        """Load model from disk"""
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
        
        print(f"✅ Model loaded from {path}")


if __name__ == '__main__':
    print("="*60)
    print("CHURN AI: MODEL TRAINING")
    print("="*60)
    
    # Import data prep
    from src.data.prepare_data import download_training_data
    
    # Step 1: Load data
    print("\n1️⃣ Loading data...")
    df = download_training_data()
    
    if df is None:
        print("❌ Failed to load data")
        exit(1)
    
    # Step 2: Engineer features
    print("\n2️⃣ Engineering features...")
    df_features = FeatureEngineer.engineer_features(df)
    X, y, feature_cols = FeatureEngineer.select_features_for_model(df_features)
    
    # Step 3: Train
    print("\n3️⃣ Training model...")
    predictor = ChurnPredictorModel()
    predictor.feature_names = feature_cols
    auc = predictor.train(X, y)
    
    # Step 4: Save
    print("\n4️⃣ Saving model...")
    predictor.save('models/churn_model.pkl')
    
    # Step 5: Test
    print("\n5️⃣ Testing predictions...")
    X_sample = X.iloc[:3]
    preds = predictor.predict(X_sample)
    
    print("\nSample predictions:")
    for i in range(len(X_sample)):
        print(f"  Customer {i+1}: {preds['churn_probability'][i]}% ({preds['risk_level'][i]} risk)")
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE")
    print("="*60)

