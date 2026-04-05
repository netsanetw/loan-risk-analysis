"""
simulation_engine.py
--------------------
Simulation Engine for Loan Limit Rules.

For every customer and each of their loans (ordered chronologically):
  1. Compute AllowedLimit  = current_multiplier × MonthlySalary
  2. Record whether the loan would have been approved (LoanAmount <= AllowedLimit)
  3. Update the multiplier for the NEXT loan:
       - On-time repayment  →  multiplier += STEPWISE_INCREASE  (capped at MAX_CAP)
       - Late repayment     →  multiplier  = PENALTY_RESET
"""

import pandas as pd
import os

# ── Rule constants ─────────────────────────────────────────────────────────────
from src.config import STARTING_TIER, MAX_CAP, STEPWISE_INCREASE, PENALTY_RESET


# ── Helpers ────────────────────────────────────────────────────────────────────

def _update_multiplier(current: float, late_payment: bool) -> float:
    """Return the multiplier to apply to the *next* loan."""
    if late_payment:
        return PENALTY_RESET
    else:
        return min(current + STEPWISE_INCREASE, MAX_CAP)


# ── Core simulation ────────────────────────────────────────────────────────────

def simulate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the loan-limit simulation over a cleaned loan-history DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain at least the columns:
        CustomerID, MonthlySalary, LoanAmount, DisbursementDate, LatePayment

    Returns
    -------
    pd.DataFrame
        Original DataFrame augmented with two new columns:
        - Multiplier    : the tier multiplier that was active for that loan
        - AllowedLimit  : MonthlySalary × Multiplier
        - Approved      : True if LoanAmount <= AllowedLimit
    """
    # Work on a copy so we never mutate the caller's DataFrame
    df = df.copy()

    # Ensure LatePayment is boolean
    #df["LatePayment"] = df["LatePayment"].astype(str).str.strip().str.lower() == "true"

    # Sort so loans are processed in chronological order within each customer
    df = df.sort_values(["CustomerID", "DisbursementDate"]).reset_index(drop=True)

    multiplier_col  = []
    allowed_col     = []
    approved_col    = []

    # ── Main loop: iterate customer by customer ────────────────────────────────
    for customer_id, group in df.groupby("CustomerID", sort=False):

        # Every new customer starts at STARTING_TIER
        multiplier = STARTING_TIER

        for _, row in group.iterrows():
            salary       = row["MonthlySalary"]
            loan_amount  = row["LoanAmount"]
            late_payment = row["LatePayment"]

            # Step 1 – Calculate AllowedLimit for THIS loan
            allowed_limit = multiplier * salary

            # Step 2 – Would the loan have been approved?
            approved = loan_amount <= allowed_limit

            # Record results for this row
            multiplier_col.append(multiplier)
            allowed_col.append(allowed_limit)
            approved_col.append(approved)

            # Step 3 – Update multiplier for the NEXT loan
            multiplier = _update_multiplier(multiplier, late_payment)

    # Attach new columns (index already matches because we reset_index above)
    df["Multiplier"]   = multiplier_col
    df["AllowedLimit"] = allowed_col
    df["Approved"]     = approved_col

    return df


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Resolve paths relative to this file so the script works from any cwd
    base_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "clean_loan_history.csv")
    out_path  = os.path.join(base_dir, "data", "simulation_results.csv")

    print(f"Loading data from: {data_path}")
    raw = pd.read_csv(data_path)

    results = simulate(raw)

    # ── Pretty-print a summary ─────────────────────────────────────────────────
    print("\n===== Simulation Results =====\n")
    display_cols = [
        "CustomerID", "DisbursementDate", "MonthlySalary",
        "LoanAmount", "Multiplier", "AllowedLimit", "LatePayment", "Approved",
    ]
    print(results[display_cols].to_string(index=False))

    # ── Per-customer summary ───────────────────────────────────────────────────
    print("\n===== Per-Customer Summary =====\n")
    summary = (
        results.groupby("CustomerID")
        .agg(
            TotalLoans      = ("LoanAmount",   "count"),
            ApprovedLoans   = ("Approved",     "sum"),
            LatePayments    = ("LatePayment",  "sum"),
            FinalMultiplier = ("Multiplier",   "last"),
        )
        .reset_index()
    )
    print(summary.to_string(index=False))

    # ── Save to CSV ────────────────────────────────────────────────────────────
    results.to_csv(out_path, index=False)
    print(f"\nResults saved to: {out_path}")
