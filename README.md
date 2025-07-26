## GTM Playbook Strategy — Synthetic MoneyMap Project
MoneyMap-style dashboard and lead scoring using a synthetic go-to-market (GTM) dataset.

# Overview
This project simulates a go-to-market optimization strategy for a B2B SaaS company. It includes:

Predicting Expected Revenue for inbound leads using machine learning

Scoring leads with a MoneyMap-style metric: PredictedRevenue / (MarketingSpend + 1)

Aggregating insights by Region and Product

Generating a dashboard with performance charts and a top-lead leaderboard

# How to Run

python sales_optimization.py


# Output
model_results.txt — Includes model performance (MSE, R²) and a leaderboard of top 10 leads by MoneyMap Score

gtm_dashboard.png — Visual dashboard with:

MoneyMap Score by Region & Product

Revenue vs Marketing Spend

Revenue by Product

Top 10 Leads by MoneyMap Score

# Input Data Format
Ensure your CSV file (synthetic_gtm_data.csv) has the following columns:

LeadID

Region

CustomerSegment

Product

DealSize

MarketingSpend

LeadScore

ExpectedRevenue

# Tools Used
Python

pandas, NumPy

scikit-learn (RandomForestRegressor)

matplotlib, seaborn

# Final Notes
The data is synthetic and used only for demonstration purposes

Can be extended to real GTM scoring use cases with geographic or segment prioritization