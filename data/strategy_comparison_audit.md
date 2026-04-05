# 📊 Strategy Comparison Audit Report

## 1. Summary Metrics

| Metric | Value |
| :--- | :--- |
| **Total Loans Evaluated** | 14 |
| **Strategy Approval Rate** | 100.0% |
| **✅ Successes (Approved & Paid)** | 7 |
| **🛑 Avoidances (Rejected & Defaulted)** | 0 |
| **⚠️ Leakages (Approved & Defaulted)** | 7 |
| **❌ Missed Opportunities (Rejected & Paid)** | 0 |

## 2. Detailed Gap Analysis

| CustomerID   |   previous_loans |   LoanAmount |   AllowedLimit | LatePayment   | Approved   |
|:-------------|-----------------:|-------------:|---------------:|:--------------|:-----------|
| C001         |                0 |          500 |           1250 | False         | True       |
| C001         |                1 |          400 |           2500 | False         | True       |
| C001         |                2 |          450 |           3750 | True          | True       |
| C002         |                0 |          700 |           1600 | True          | True       |
| C002         |                1 |          800 |           1600 | False         | True       |
| C003         |                0 |          600 |           1400 | True          | True       |
| C003         |                1 |          500 |           1400 | False         | True       |
| C004         |                0 |         1000 |           2000 | False         | True       |
| C004         |                1 |         1200 |           4000 | False         | True       |
| C005         |                0 |          300 |           1100 | True          | True       |
| C007         |                0 |          200 |            900 | True          | True       |
| C008         |                0 |          900 |           1750 | False         | True       |
| C009         |                0 |          500 |           1350 | True          | True       |
| C010         |                0 |          600 |           2000 | True          | True       |

---
*Audit generated as part of the Year 2 Risk Verification Project.*