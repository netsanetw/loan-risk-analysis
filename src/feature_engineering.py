import pandas as pd

def add_history_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs historical features for each loan based on a customer's 
    past repayment behavior.
    
    Features built:
    - previous_loans: Total count of loans prior to this one.
    - previous_on_time: Count of previous loans repaid with no 30+ days past due.
    - ever_past_due: Binary flag (1 if they ever had 30+ days past due event in the past, else 0).
    """
    
    # Work on a copy to avoid mutating the original dataframe
    df = df.copy()
    
    # 1. Ensure chronological order per customer
    df['DisbursementDate'] = pd.to_datetime(df['DisbursementDate'])
    df = df.sort_values(['CustomerID', 'DisbursementDate']).reset_index(drop=True)
    
    # 2. Number of previous loans
    df['previous_loans'] = df.groupby('CustomerID').cumcount()
    
    # 3. Number of previous on-time repayments
    # We identify "on-time" as (PastDue30Days == 0). 
    # We use shift(1) to ensure we only look at PAST loans.
    df['is_on_time'] = (df['PastDue30Days'] == 0).astype(int)
    df['previous_on_time'] = df.groupby('CustomerID')['is_on_time'].cumsum().shift(1).fillna(0).astype(int)
    # Adjust for the first loan of each customer (shift across groups)
    df.loc[df.groupby('CustomerID').head(1).index, 'previous_on_time'] = 0
    
    # 4. Ever had a 30+ days past due event in the past
    # We use cummax() on the PastDue30Days flag and shift it.
    df['ever_past_due'] = df.groupby('CustomerID')['PastDue30Days'].cummax().shift(1).fillna(0).astype(int)
    # Adjust for the first loan of each customer
    df.loc[df.groupby('CustomerID').head(1).index, 'ever_past_due'] = 0
    
    # Clean up temporary helper columns
    df = df.drop(columns=['is_on_time'])
    
    return df

def add_history_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorizes each loan into a history level for evaluation:
    - Late History: ever_past_due == 1
    - No History: ever_past_due == 0 AND previous_loans == 0
    - 1-2 Good Loans: ever_past_due == 0 AND previous_loans in [1, 2]
    - 3+ Good Loans: ever_past_due == 0 AND previous_loans >= 3
    """
    df = df.copy()

    def segment(row):
        if row['ever_past_due'] == 1:
            return 'Late History'
        elif row['previous_loans'] == 0:
            return 'No History'
        elif row['previous_loans'] <= 2:
            return '1-2 Good Loans'
        else:
            return '3+ Good Loans'

    df['HistoryLevel'] = df.apply(segment, axis=1)
    return df

if __name__ == "__main__":
    # Example usage / testing
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "clean_loan_history.csv")
    
    if os.path.exists(data_path):
        raw_data = pd.read_csv(data_path)
        enriched_data = add_history_features(raw_data)
        print("Enriched Data Snippet (C001):")
        print(enriched_data[enriched_data['CustomerID'] == 'C001'][['CustomerID', 'previous_loans', 'previous_on_time', 'ever_past_due']])
