# Database schema

The logical model is defined in the blueprint. Initial migrations are intentionally split by bounded context:

- `001_initial.sql`: productivity tables and shared metadata.
- `002_finance.sql`: assets, confirmed investment ledger, recurring plans, snapshots.
- `003_expenses.sql`: cash transactions, categories, budgets, imports, reconciliation.

Money is stored as integer minor units or exact decimal strings; timestamps are UTC and user-facing dates are local dates. Foreign keys, unique constraints, and explicit reversal records are required.
