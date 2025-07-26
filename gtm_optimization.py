import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

sns.set_style("darkgrid")

def load_data():
    return pd.read_csv("synthetic_gtm_data.csv")

def train_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_pred

def main():
    data = load_data()
    features = ['DealSize','MarketingSpend','LeadScore']
    X = data[features]
    y = data['ExpectedRevenue']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    mse, r2, y_pred = evaluate_model(model, X_test, y_test)

    data['PredictedRevenue'] = model.predict(data[features])
    data['MoneyMapScore'] = data['PredictedRevenue'] / (data['MarketingSpend']+1)

    # Profit cube analog: aggregated
    agg = data.groupby(['Region','Product']).agg({
        'MoneyMapScore': 'sum',
        'PredictedRevenue': 'sum',
        'MarketingSpend':'sum'
    }).reset_index()

    # Save results
    top10 = data.nlargest(10, 'MoneyMapScore')[[
        'LeadID','Region','CustomerSegment','Product',
        'DealSize','MarketingSpend','LeadScore','PredictedRevenue','MoneyMapScore'
    ]]

    top10['ShortLeadID'] = top10['LeadID'].astype(str).str[:8]
    output = StringIO()
    output.write(f"Model MSE: {mse:.2f}\nR2 Score: {r2:.3f}\n\nTop 10 MoneyMap Scored Leads:\n")
    top10.to_string(buf=output, index=False)
    with open("model_results.txt","w") as f:
        f.write(output.getvalue())
    print("Results saved to model_results.txt")

    # Dashboard plots
    fig, axes = plt.subplots(2,2, figsize=(18,14))
    sns.barplot(data=agg, x='Region', y='MoneyMapScore', hue='Product', ax=axes[0,0])
    axes[0,0].set_title('MoneyMap Score by Region & Product')

    sns.scatterplot(data=data, x='MarketingSpend', y='PredictedRevenue', hue='Region', ax=axes[0,1])
    axes[0,1].set_title('Revenue vs Marketing Spend')

    sns.barplot(data=agg, x='Product', y='PredictedRevenue', ax=axes[1,0], palette='viridis')
    axes[1,0].set_title('Predicted Revenue by Product')

    sns.barplot(
    data=top10.sort_values('MoneyMapScore'),
    x='MoneyMapScore', y='ShortLeadID', ax=axes[1,1], palette='magma'
    )
    axes[1,1].set_title('Top 10 Leads (MoneyMap Score)')
    axes[1,1].tick_params(axis='y', labelsize=10)
    plt.tight_layout(pad=4.0)
    plt.subplots_adjust(hspace=0.3,wspace=0.3)
    plt.savefig("gtm_dashboard.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__=="__main__":
    main()
