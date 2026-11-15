# LifeOS engineering rules

- Keep the application a modular monolith; do not introduce cloud services or microservices for MVP.
- Use `Decimal` or integer minor units for money. Never use binary floats for financial values.
- Treat confirmed transactions as the source of truth; never overwrite historical holdings.
- Require explicit confirmation before an investment affects holdings.
- Keep sensitive data local, encrypted, and absent from logs, fixtures, screenshots, and telemetry.
- Request only the permissions required by the feature. No SMS, contacts, location, accessibility, or broad storage permissions in MVP.
- Add migrations, tests, and rollback behavior with persistence changes.
- Do not claim Android compatibility without testing on actual hardware.
