# ============================================================
# Loan Risk Analysis - Rule Parameters / Constants
# ============================================================
# These constants define the loan limit tier rules based on
# a borrower's repayment behaviour (as a multiplier of
# their monthly salary).

# The initial loan limit assigned to every borrower
STARTING_TIER: float = 0.5       # 0.5x monthly salary

# The absolute maximum loan limit a borrower can reach
MAX_CAP: float = 3.0             # 3.0x monthly salary

# Amount the loan limit increases after each on-time repayment
STEPWISE_INCREASE: float = 0.15   # +0.5x monthly salary per good repayment

# Amount the loan limit is penalised / reset by after a late payment
PENALTY_RESET: float = 0.15     # Reset back to 0.5x monthly salary
