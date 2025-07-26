import pandas as pd
import numpy as np

np.random.seed(42)
n = 2000  # leads

regions = ['North', 'South', 'East', 'West']
segments = ['SMB', 'MidMarket', 'Enterprise']
industries = ['Retail', 'Finance', 'Healthcare', 'Tech', 'Manufacturing']
products = ['Analytics', 'CRM', 'ERP']

data = pd.DataFrame({
    'LeadID': range(1, n+1),
    'Region': np.random.choice(regions, n),
    'CustomerSegment': np.random.choice(segments, n, p=[0.5,0.3,0.2]),
    'Industry': np.random.choice(industries, n),
    'Product': np.random.choice(products, n),
    'DealSize': np.round(np.random.normal(20000, 7000, n)).clip(2000, 100000),
    'MarketingSpend': np.round(np.random.uniform(500, 3000, n), 0),
    'LeadScore': np.round(np.random.beta(2,5, n), 2),
    'Converted': np.random.binomial(1, 0.3, n)
})
data['ConversionRate'] = data.groupby(['Region','Product'])['Converted'].transform('mean')
data['ExpectedRevenue'] = data['DealSize'] * data['ConversionRate']
data.to_csv("synthetic_gtm_data.csv", index=False)
print("Saved synthetic_gtm_data.csv")