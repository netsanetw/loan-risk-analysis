import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np

def train_risk_model(df):
    """
    Trains a Logistic Regression model to predict the probability of 
    a late payment based on customer and loan features.
    """
    # 1. Select features and target
    # We use historical behavior and current loan details
    features = ['MonthlySalary', 'LoanAmount', 'previous_loans', 'ever_past_due']
    target = 'LatePayment'
    
    # 2. Filter data (ensure no NaNs in training)
    df_train = df.dropna(subset=[target] + features)
    
    if df_train.empty:
        raise ValueError("No data available for training. Ensure the DataFrame is cleaned and enriched.")
    
    X = df_train[features]
    y = df_train[target].astype(int)
    
    # 3. Initialize and train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    
    print(f"Logistic Regression Model trained on {len(df_train)} rows.")
    return model

def apply_risk_scoring(df, model):
    """
    Applies the trained model to a DataFrame to calculate risk scores 
    and categories.
    """
    df = df.copy()
    features = ['MonthlySalary', 'LoanAmount', 'previous_loans', 'ever_past_due']
    
    # 1. Predict probability of default (PD)
    # predict_proba returns [prob_0, prob_1], we want prob_1 (LatePayment == True)
    df['RiskProbability'] = model.predict_proba(df[features])[:, 1]
    
    # 2. Map Probability to Risk Categories
    def categorize_risk(prob):
        if prob < 0.2:
            return 'Low'
        elif prob < 0.5:
            return 'Medium'
        else:
            return 'High'
            
    df['RiskCategory'] = df['RiskProbability'].apply(categorize_risk)
    
    return df
