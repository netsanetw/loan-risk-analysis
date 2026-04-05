import pandas as pd
import os

def clean_data(df):
    """
    Cleans the loan history data by converting dates, numeric fields, 
    and creating a LatePayment flag.
    """
    # Convert dates
    df['DisbursementDate'] = pd.to_datetime(df['DisbursementDate'])
    df['DueDate'] = pd.to_datetime(df['DueDate'])
    df['ActualRepaymentDate'] = pd.to_datetime(df['ActualRepaymentDate'])

    # Convert numeric fields
    df['PastDue30Days'] = pd.to_numeric(df['PastDue30Days'], errors='coerce')

    # Create LatePayment flag
    df['LatePayment'] = df['PastDue30Days'] > 0

    return df

def handle_missing_values(df, output_path):
    """
    Identifies rows with missing values, saves them to a separate CSV,
    and returns a DataFrame with those rows removed.
    """
    # Identify rows with any missing values
    missing_mask = df.isnull().any(axis=1)
    df_missing = df[missing_mask]
    df_clean = df[~missing_mask]

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Always save the CSV (even if empty, it will contain headers)
    df_missing.to_csv(output_path, index=False)

    if not df_missing.empty:
        print(f"Found {len(df_missing)} rows with missing values. Saved to: {output_path}")
    else:
        print(f"No missing values found. Created empty file with headers at: {output_path}")


    return df_clean