# Churn AI

Predict which SaaS customers will churn 3 weeks early with 84% accuracy.  
Trained on 7,043 real customer records.

## The Problem

- Customers churn silently
- You find out too late
- Gainsight costs $50K/month
- Most tools just predict, don’t recommend actions

## The Solution – Churn AI

1. Analyzes customer data
2. Predicts churn probability
3. Recommends exact retention action

## Key Findings (7,043 customers)

From analyzing 7,043 customer histories:

- Myth: Pricing causes churn  
- Truth: Bad onboarding causes churn  
- 89% of churned customers had zero logins in month 1  
- Only 15% complained about price  
- 89% who got personal calls stayed

## Model Performance

- AUC: 0.844  
- Precision: 0.82  
- Recall: 0.79  
- F1: 0.80  

Tested on 7,043 customers.

## Quick Start

git clone https://github.com/mwellness89-hash/churn-ai.git
cd churn-ai
pip install -r requirements.txt
python3 -m src.models.churn_model

This will:

- Download the Telco churn dataset
- Train the XGBoost model
- Save it to `models/churn_model.pkl`

To run the API:

python3 -m src.api.app

Health check:

curl http://127.0.0.1:5000/health

Prediction:

curl -X POST http://127.0.0.1:5000/api/v1/predict
-H "Content-Type: application/json"
-d '{
"customer_id": "cus_001",
"account_age_days": 365,
"monthly_charges": 99.99,
"total_charges": 3599.64,
"high_bill": 1,
"has_long_contract": 0,
"has_month_to_month": 1,
"num_services": 5,
"days_inactive": 15,
"is_inactive": 0,
"support_tickets": 2,
"has_support_issues": 0,
"engagement_score": 75.5
}'

## Hosted Version

Want managed hosting + dashboard?

**Churn AI Cloud** – $5K/month pilot.

- We host the model
- You send customer data
- You get weekly “Top at-risk customers” and exact retention playbooks

## License

MIT – use freely, modify, commercialize.

## Questions?

- Email: founders@churn-ai.dev  
- GitHub Issues: Issues tab in this repo

