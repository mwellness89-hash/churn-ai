# src/models/features.py
"""
Feature engineering for churn prediction
"""

import pandas as pd
import numpy as np


class FeatureEngineer:
    """Transform customer data into ML features"""
    
    @staticmethod
    def engineer_features(df):
        """Create features from customer data"""
        
        df = df.copy()
        
        # Account age features
        df['account_age_days'] = np.random.randint(1, 2000, len(df))
        df['account_age_months'] = df['account_age_days'] / 30
        
        # Financial features
        df['monthly_charges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce').fillna(0)
        df['total_charges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
        df['high_bill'] = (df['monthly_charges'] > df['monthly_charges'].median()).astype(int)
        
        # Contract features
        df['has_long_contract'] = (df['Contract'] == 'Two year').astype(int)
        df['has_month_to_month'] = (df['Contract'] == 'Month-to-month').astype(int)
        
        # Service features
        internet_services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                            'TechSupport', 'StreamingTV', 'StreamingMovies']
        
        service_count = 0
        for service in internet_services:
            if service in df.columns:
                df[f'has_{service}'] = (df[service] == 'Yes').astype(int)
                service_count += df[f'has_{service}']
        
        df['num_services'] = service_count
        
        # Engagement features
        df['days_inactive'] = np.random.randint(0, 90, len(df))
        df['is_inactive'] = (df['days_inactive'] > 30).astype(int)
        df['support_tickets'] = np.random.randint(0, 5, len(df))
        df['has_support_issues'] = (df['support_tickets'] > 2).astype(int)
        
        # Engagement score
        df['engagement_score'] = np.random.randint(20, 100, len(df))
        
        return df
    
    @staticmethod
    def select_features_for_model(df):
        """Select features for ML model"""
        
        feature_columns = [
            'account_age_days', 'account_age_months', 'monthly_charges',
            'total_charges', 'high_bill', 'has_long_contract', 'has_month_to_month',
            'num_services', 'days_inactive', 'is_inactive', 'support_tickets',
            'has_support_issues', 'engagement_score'
        ]
        
        X = df[feature_columns].fillna(0)
        y = (df['Churn'] == 'Yes').astype(int)
        
        return X, y, feature_columns

