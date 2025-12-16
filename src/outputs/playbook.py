# src/outputs/playbook.py
"""
Generate retention playbooks for customers
"""

import csv
from datetime import datetime
import os


def generate_playbook(company_name, at_risk_customers):
    """
    Generate CSV with top at-risk customers and actions
    
    at_risk_customers: list of dicts with:
    - customer_id
    - customer_name
    - arr (annual recurring revenue)
    - churn_probability (0-100)
    - reason (why they're at risk)
    - discount (what to offer)
    """
    
    os.makedirs('outputs', exist_ok=True)
    
    filename = f"outputs/{company_name}_playbook_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Customer ID',
            'Customer Name',
            'ARR',
            'Churn Risk %',
            'Reason for Risk',
            'Action',
            'Discount',
            'Priority'
        ])
        
        total_arr = 0
        
        for customer in at_risk_customers:
            risk = customer['churn_probability']
            arr = customer['arr']
            total_arr += arr
            
            # Determine action based on risk
            if risk > 75:
                action = "Schedule CS call immediately"
                priority = "CRITICAL"
            elif risk > 50:
                action = "Send personalized email"
                priority = "HIGH"
            else:
                action = "Add to nurture sequence"
                priority = "MEDIUM"
            
            writer.writerow([
                customer['customer_id'],
                customer['customer_name'],
                f"${arr:,.0f}",
                f"{risk:.0f}%",
                customer['reason'],
                action,
                customer.get('discount', 'N/A'),
                priority
            ])
    
    print(f"\n✅ Playbook created: {filename}")
    print(f"📊 Total ARR at risk: ${total_arr:,.0f}")
    print(f"📋 Customers: {len(at_risk_customers)}")
    
    return filename


if __name__ == '__main__':
    # Example usage
    sample = [
        {
            "customer_id": "cus_001",
            "customer_name": "Acme Corp",
            "arr": 120000,
            "churn_probability": 85,
            "reason": "Usage down 45%, no logins 30+ days",
            "discount": "20% annual"
        },
        {
            "customer_id": "cus_002",
            "customer_name": "TechFlow Inc",
            "arr": 85000,
            "churn_probability": 62,
            "reason": "Competitor inquiry received",
            "discount": "10% + premium support"
        },
        {
            "customer_id": "cus_003",
            "customer_name": "DataSync Ltd",
            "arr": 55000,
            "churn_probability": 45,
            "reason": "Support ticket unanswered",
            "discount": "Free support 3mo"
        }
    ]
    
    generate_playbook("example_company", sample)

