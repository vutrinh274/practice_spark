# Ledger Reconciliation

**Difficulty:** Hard
**Tags:** full outer join, variance

## Background

The finance team needs to reconcile the internal system ledger against the bank statement. Some transactions match exactly, some have amount discrepancies, and some appear in only one source.

## Schema

**system_ledger** (`system_ledger.csv`)

| Column | Type | Description |
|---|---|---|
| txn_id | INT | Transaction identifier |
| amount | DOUBLE | Amount recorded in the system |
| category | STRING | Expense category |

**bank_ledger** (`bank_ledger.csv`)

| Column | Type | Description |
|---|---|---|
| txn_id | INT | Transaction identifier |
| amount | DOUBLE | Amount recorded by the bank |
| category | STRING | Expense category |

## Task

Identify all **discrepancies** between the two ledgers. A discrepancy exists when:
- The amounts differ for the same `txn_id`, OR
- A transaction appears in only one ledger (NULL on the other side).

Compute `variance = bank_amount - system_amount`. If either side is NULL, `variance` should also be NULL.

Return: **txn_id, system_amount, bank_amount, variance**
Order by: **txn_id ASC**

## Expected Discrepancies

| txn_id | system_amount | bank_amount | variance |
|---|---|---|---|
| 1002 | 80.50 | 82.00 | 1.50 |
| 1004 | 45.00 | NULL | NULL |
| 1006 | 150.00 | 155.00 | 5.00 |
| 1008 | 500.00 | 510.00 | 10.00 |
| 1010 | 275.00 | NULL | NULL |
| 1011 | NULL | 400.00 | NULL |
| 1012 | NULL | 35.00 | NULL |

## Notes

- Transactions 1001, 1003, 1005, 1007, 1009 match exactly — exclude them.
- Transaction 1004 and 1010 are only in the system ledger.
- Transactions 1011 and 1012 are only in the bank ledger.
