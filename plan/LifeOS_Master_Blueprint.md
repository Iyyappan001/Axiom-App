# LifeOS — Master Product & Engineering Blueprint

**Version:** 1.0 | **Date:** 15 November 2026 | **Status:** Planning reference

## 1. Product vision and decisions

LifeOS is a personal, Android-only, offline-first operating system for daily productivity, financial assets, spending, habits, and goals. The name **LifeOS** is provisional. The app will be built primarily with **Python + Kivy**, distributed as a privately signed Android APK, and use an **encrypted on-device SQLite database (SQLCipher)**. No cloud account or cloud sync in MVP. Internet access is optional for public stock, ETF and mutual-fund price updates. User-entered financial data must not be transmitted to price providers.

**Primary user workflows:** Plan a day/week; complete tasks and earn XP; manage habits and milestones; enter mutual fund, stock, ETF, EPF and bank account data manually; configure monthly investment schedules; confirm actual investments; record expenses and transfers; review portfolio, cash and goal progress.

**Out of scope for MVP:** Bank login integration, UPI PINs/OTPs, SMS reading, notification-listener access, cloud synchronization, financial advice automation, AI assistant, multi-user support. SMS expense parsing may be evaluated later following a separate Android permission and security review.

## 2. Product modules

### 2.1 Home dashboard
- Today's top priorities, task completion count, earned XP, habit streaks.
- Total financial assets, recent spending, goal progress and alerts for stale balances.
- Bottom navigation: **Home / Tasks / Finance / Habits / Goals**. Analytics and Settings accessible from secondary navigation.

### 2.2 Tasks and weekly planning
- Task CRUD; description, category, priority, difficulty, importance, estimated duration, due date, recurrence and status.
- Daily and weekly plans, planned vs completed reporting, recurring tasks and completion history.
- Suggested XP formula: `XP = 10 + 5*difficulty + 5*importance` with both inputs 1–5. XP awarded exactly once per completion and persisted in an XP ledger. Reversals must be explicit.
- Streaks based on meaningful habit/task completion, not opening the app; no incentives for trivial task spam.

### 2.3 Investments and financial assets
- **Mutual funds:** scheme/AMFI code, folio label, purchase/redemption transactions, units, NAV, valuation date, invested amount, absolute gain, XIRR where cash-flow history is sufficient.
- **Stocks/ETFs:** exchange, ticker, ISIN if known, quantity, cost basis, fees, taxes, buy/sell transactions, dividends, market price, realized/unrealized returns.
- **EPF:** opening balance, employee contribution, employer EPF contribution, interest credited and adjustments; distinguish EPS pension from EPF assets.
- **Bank accounts:** bank name, masked identifier, currency, verified balance and dated snapshots; no credentials or full account numbers required.
- **Liabilities (optional early, planned):** home/gold loans, interest, outstanding balance and snapshots, enabling net worth.
- **Metrics:** total financial assets, invested corpus, liquid cash, asset allocation, investment gain, net worth (assets minus liabilities), cash-flow history and monthly snapshots. Keep ₹1 crore investable-corpus goal separate from property-inclusive net worth.

### 2.4 Recurring investments
- Configure monthly amount, day, asset/account and active status for SIPs or regular purchases.
- Generate **pending planned** investment entries, not confirmed purchases. Confirm using actual date, amount, units and NAV/price before affecting holdings.
- Ensure `(recurring_id, due_month)` is unique and generation is idempotent; reconcile missed months on app startup if Android background work is delayed.
- Record every transaction in a durable ledger; calculate holdings from confirmed transactions rather than overwriting a balance.

### 2.5 Expenses and budgets
- Manual income/expense entry, categories, budgets, account mapping and monthly trends.
- CSV statement import with preview, normalization, duplicate detection and reconciliation.
- Internal bank transfers are **not income or expenses**; investment purchases are asset transfers, not consumption; loan repayments separate principal from interest; refunds adjust expenses.
- SMS import is deferred. If introduced, perform parsing locally, minimize permissions, exclude OTPs and do not upload raw messages.

### 2.6 Habits, goals and analytics
- Habits: reading, meditation, exercise, learning, recurrence, daily logs and streaks.
- Goals: personal, career, financial and health; milestones, target dates, progress and status.
- Analytics: weekly task completion, XP, habit consistency, monthly spending, savings rate, allocation, historical net worth and corpus progress.

## 3. Technology stack and constraints

| Layer | Selected approach |
|---|---|
| Android app/UI | Python 3, Kivy; optional KivyMD only after compatibility test |
| Persistence | SQLite via SQLCipher-compatible Android Python binding (must validate packaging) |
| Key management | Android Keystore through Java/Kotlin bridge and PyJNIus |
| Unlock | Android BiometricPrompt + supported device credential |
| Finance math | Python `decimal.Decimal`, `datetime`, exact dated cash flows |
| Market prices | HTTPS provider adapters; response validation and dated cache |
| Quality | pytest, Ruff, dependency audit, integration/device tests |
| APK | Buildozer + python-for-android on Linux CI; signed release |
| Development | VS Code + Python venv on Apple Silicon Mac, physical Android test phone |

Architecture: **modular monolith**. UI -> application services -> domain logic -> repositories -> encrypted local database. Market data and Android native features are separate adapters. Avoid microservices and a cloud backend.

**Feasibility gates:** (1) Kivy APK launches on actual Android hardware; (2) SQLCipher binding packages and encrypts successfully; (3) Keystore/BiometricPrompt bridge works; (4) encrypted backup restores on a second device. Do not use real financial data before all pass.

## 4. Target repository structure

```text
lifeos/
├── README.md
├── AGENTS.md
├── CLAUDE.md                       # only if using Claude Code
├── pyproject.toml
├── buildozer.spec
├── .gitignore
├── .env.example
├── Makefile
├── .github/workflows/
│   ├── python-tests.yml
│   ├── security-checks.yml
│   └── android-build.yml
├── .agents/skills/
│   ├── python-engineering/SKILL.md
│   ├── android-kivy/SKILL.md
│   ├── database-security/SKILL.md
│   ├── android-security/SKILL.md
│   ├── finance-engine/SKILL.md
│   ├── productivity-engine/SKILL.md
│   ├── ui-ux-design/SKILL.md
│   ├── testing-qa/SKILL.md
│   └── android-build-release/SKILL.md
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── SECURITY.md
│   ├── BACKUP_RECOVERY.md
│   ├── UI_DESIGN.md
│   ├── API_INTEGRATIONS.md
│   ├── TEST_PLAN.md
│   └── RELEASE_CHECKLIST.md
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── bootstrap.py
│   ├── config.py
│   ├── core/{events.py,exceptions.py,clock.py,scheduler.py}
│   ├── ui/
│   │   ├── {app_shell.py,navigation.py,theme.py}
│   │   ├── screens/
│   │   │   ├── {onboarding.py,unlock.py,home.py,daily_tasks.py,weekly_planner.py}
│   │   │   ├── {task_editor.py,finance_dashboard.py,investment_list.py}
│   │   │   ├── {investment_detail.py,investment_editor.py,bank_accounts.py,epf.py}
│   │   │   └── {expenses.py,habits.py,goals.py,analytics.py,settings.py}
│   │   ├── components/
│   │   │   ├── {metric_card.py,task_card.py,investment_card.py}
│   │   │   └── {progress_bar.py,chart_card.py,bottom_navigation.py,confirmation_dialog.py}
│   │   └── kv/{home.kv,tasks.kv,finance.kv,theme.kv}
│   ├── modules/
│   │   ├── productivity/{models.py,service.py,scoring.py,streaks.py,planning.py}
│   │   ├── finance/
│   │   │   ├── {models.py,service.py,portfolio.py,transactions.py,recurring.py}
│   │   │   └── {valuation.py,returns.py,epf.py,bank_accounts.py,net_worth.py}
│   │   ├── expenses/{models.py,service.py,categories.py,budgets.py,reconciliation.py,csv_import.py}
│   │   ├── habits/{models.py,service.py,streaks.py}
│   │   ├── goals/{models.py,service.py,milestones.py}
│   │   └── analytics/{productivity.py,finance.py,reports.py}
│   ├── data/
│   │   ├── {connection.py,schema.py,unit_of_work.py}
│   │   ├── migrations/{001_initial.sql,002_finance.sql,003_expenses.sql}
│   │   └── repositories/
│   │       ├── {task_repository.py,finance_repository.py,expense_repository.py}
│   │       └── {habit_repository.py,goal_repository.py}
│   ├── security/
│   │   ├── {encryption.py,keystore.py,authentication.py,session_lock.py}
│   │   └── {backup.py,restore.py,logging.py}
│   ├── integrations/{market_prices.py,mutual_fund_nav.py,android_bridge.py}
│   └── assets/{icons/,images/,fonts/}
├── android/
│   ├── native/{LifeOSSecurityBridge.java,LifeOSBackupBridge.java}
│   ├── manifest/
│   └── data_extraction_rules.xml
├── scripts/{validate_schema.py,seed_demo_data.py,check_dependencies.py,verify_release.py}
├── tests/
│   ├── conftest.py
│   ├── unit/{test_task_scoring.py,test_streaks.py,test_portfolio.py}
│   ├── unit/{test_recurring_investments.py,test_epf.py,test_expenses.py}
│   ├── integration/{test_database.py,test_migrations.py,test_backup_restore.py}
│   └── android/{test_biometrics.md,test_permissions.md,test_apk_release.md}
└── tools/linux-build/Dockerfile
```

Brace groups above are shorthand for separate files; create files incrementally, not all as empty placeholders. Confirm coding-assistant skill discovery conventions for your actual tool/version.

## 5. Database schema — logical model

### Productivity
| Table | Core fields |
|---|---|
| tasks | id, title, description, category, difficulty, importance, priority, due_at, status |
| task_schedules | id, task_id, planned_date, recurrence_rule |
| task_completions | id, task_id, completed_at, xp_awarded |
| xp_ledger | id, source_type, source_id, xp_delta, created_at |
| habits | id, name, frequency, target_count, active |
| habit_logs | id, habit_id, log_date, completed_count |
| goals | id, name, category, target_value, target_date |
| milestones | id, goal_id, title, target_date, status |

### Finance
| Table | Core fields |
|---|---|
| assets | id, asset_type, name, ticker, exchange, isin, scheme_code, currency |
| investment_accounts | id, provider, account_type, masked_identifier |
| investment_transactions | id, asset_id, account_id, type, trade_date, units, price, fees, amount |
| recurring_investments | id, asset_id, account_id, amount, day_of_month, active |
| scheduled_investments | id, recurring_id, due_month, status, confirmed_transaction_id |
| market_prices | asset_id, price, price_date, source |
| bank_accounts | id, bank_name, masked_identifier, currency, active |
| bank_balance_snapshots | id, bank_account_id, balance, as_of |
| epf_accounts | id, employer_label, opening_balance, opening_date |
| epf_entries | id, epf_account_id, entry_date, employee_amount, employer_epf_amount, interest_amount, entry_type |
| liabilities | id, liability_type, name, balance, interest_rate |
| liability_snapshots | id, liability_id, snapshot_date, outstanding_balance |
| financial_snapshots | id, snapshot_date, investment_value, epf_value, bank_cash, liabilities, net_worth |

### Expenses
| Table | Core fields |
|---|---|
| expense_categories | id, name, parent_id |
| cash_transactions | id, account_id, amount, direction, category_id, date, description, transfer_group_id |
| budgets | id, category_id, month, limit_amount |
| import_batches | id, source, imported_at, checksum |
| transaction_matches | id, cash_transaction_id, external_reference, match_status |

**Data invariants:** Use foreign keys and migrations; amounts as integer minor units or exact decimal strings (never float); high-precision units/NAV; UTC timestamps with local dates where relevant; transaction ledger as source of truth; uniqueness on scheduled investments by recurring ID/month; snapshots dated and source-attributed; historical price dates shown to users. Design explicit reversals rather than silently rewriting historical records.

## 6. Security implementation plan

### 6.1 Threat model
Protect against casual unauthorized access, lost/stolen phone, accidental backups/log leaks, malicious or vulnerable dependencies, insecure network calls, APK tampering and data loss. Rooted or fully compromised devices are outside strong guarantees; local-only storage does not eliminate all risk.

### 6.2 Encryption and keys
1. Generate a random 256-bit SQLCipher database key on first launch.
2. Create a non-exportable AES key in Android Keystore, hardware-backed when available.
3. Wrap the database key with AES-GCM using a unique nonce; store only wrapped key + metadata in app-private storage.
4. Require Android biometric/device-credential authentication to authorize unwrap, using BiometricPrompt and a native bridge; confirm the exact Keystore authentication policy works on supported Android versions.
5. Open SQLCipher only after key unwrap; never hardcode key or log it. Close/relock on background and timeout where feasible; acknowledge in-memory secrets may remain briefly.
6. Test the actual SQLCipher Android binding; standard `sqlite3` is not encrypted.

### 6.3 Local storage and permissions
- Store database and metadata only in Android private internal app storage; verify Kivy's `user_data_dir` path on device.
- Exclude database and key metadata from Android auto-backup/device-transfer rules unless a tested scheme supports them.
- MVP permissions: Internet only if price updates are enabled; native biometric API as required. No SMS, notification listener, contacts, camera, microphone, location, accessibility or broad storage permissions.
- Use Android document picker for user-initiated imports/exports.

### 6.4 UI/session safety
- BiometricPrompt or device credential; no custom insecure PIN gate.
- Auto-lock on background and after ~2 minutes inactivity; reauthenticate on process restart.
- Use Android `FLAG_SECURE` for sensitive windows and recents preview; test screen recording. This does not prevent photography or device compromise.
- Never log balances, transaction payloads, account identifiers, keys, tokens or recovery passwords. Redact Python, Kivy and Android logs.

### 6.5 Encrypted backup and recovery
- Portable, versioned encrypted export using authenticated encryption (AES-256-GCM), password-derived key (Argon2id with tested device-appropriate parameters), fresh salt and nonce.
- Back up a consistent database snapshot; avoid writing plaintext temporary copies to shared storage.
- Export via system document picker. Restore only after validating authentication tag, version and database integrity; preserve existing database on failed restore.
- Recovery passphrase must be kept outside phone. Android Keystore keys are device-bound; don't assume they can migrate.
- Test restoration on a different physical Android device before real data entry.

### 6.6 Network and release
- HTTPS only; certificate verification on; trusted domain allowlist, response schema/range/date checks and timeouts. Never send private holdings or balances to market-price APIs.
- Pin dependencies; review python-for-android recipes and transitive native packages; audit known vulnerabilities.
- Build on pinned Linux CI, run tests, inspect manifest/permissions, disable debug, sign release with protected key, verify signature and install on test phone.
- Protect signing secrets outside source control; keep private Git repository; no actual financial data in fixtures.

## 7. AI coding instructions and skills

**Master `AGENTS.md`:** Python-first modular monolith; no sensitive plaintext; no hardcoded secrets; Decimal for finance; transaction-based holdings; explicit user confirmation for investments; offline-first; no unnecessary permissions; automated tests and migrations; no claims of Android compatibility without real-device evidence.

Recommended skills:
1. `python-engineering`: architecture, typing, exceptions, Ruff, packaging.
2. `android-kivy`: responsive screens, navigation, lifecycle, device constraints.
3. `database-security`: SQLCipher, keys, schema migration, encrypted backup.
4. `android-security`: BiometricPrompt, Keystore, permissions, `FLAG_SECURE`.
5. `finance-engine`: exact money math, XIRR, purchases/sales, SIP idempotency, EPF.
6. `productivity-engine`: task rules, XP, streaks, recurring plans.
7. `ui-ux-design`: components, contrast, touch targets, dashboards.
8. `testing-qa`: unit/integration/device/security regression tests.
9. `android-build-release`: Buildozer, CI, signing, APK verification.

Skills are AI instructions, **not security controls**. Use actual implementation, code review and tests for enforcement. Claude Code may need `.claude/skills/` instead of `.agents/skills/`; verify tool discovery.

## 8. UI design system

- Dark-first with accessible light option; sample colors: background `#111827`, surface `#1F2937`, primary `#5B8DEF`, positive `#20B486`, accent `#F4B860`.
- 8-point spacing scale, readable typography, 44–48 dp minimum touch targets, consistent cards and dialogs.
- Finance screens show last-updated timestamp, source and pending/confirmed status. No unlabeled charts or implied live data.
- Key screens: onboarding, unlock, home, daily tasks, weekly planner, task editor, finance dashboard, investment list/detail/editor, bank accounts, EPF, expenses, habits, goals, analytics, settings, backup/restore.

## 9. Development workflow and milestones

| Phase | Target | Exit criterion |
|---|---|---|
| 1. Foundation | Week 1 | Minimal Kivy app launches on physical Android |
| 2. Security | Weeks 2–3 | SQLCipher, Keystore, biometric lock, backup and restore tested |
| 3. Productivity MVP | Weeks 4–5 | Tasks, daily/weekly planning, XP and streaks usable |
| 4. Finance | Weeks 6–7 | Holdings, recurring plans, EPF and bank accounts work |
| 5. Expenses/goals | Weeks 8–9 | Manual expenses, CSV import, habits, milestones work |
| 6. Analytics/polish | Week 10 | Reports, design system and accessibility verified |
| 7. Release | Weeks 11–12 | Security tests and signed APK pass |

Estimates are aspirational part-time milestones; Android security bridging and native SQLCipher packaging may extend them.

**Recommended first vertical slice:** signed prototype APK, biometric unlock, encrypted DB, one fictional task, one fictional investment, restart persistence and cross-device encrypted backup restore. Do not enter real financial data before it passes.

## 10. Testing and acceptance criteria

### Unit tests
- XP once per completion, scoring and reversals; streak boundary cases; weekly recurring tasks.
- Decimal math, buy/sell/redemption, dividends, XIRR, stale NAV, EPF contributions and bank balances.
- Monthly schedule idempotency across retries, missed months and app restarts.
- Transfers/refunds/loan repayments not double-counted; CSV duplicate detection.

### Integration tests
- Encrypted DB refuses wrong key; standard SQLite cannot read it.
- Foreign keys, migrations, rollback on failure, consistent financial snapshots.
- Backup decrypts only with correct passphrase, restore works on another device and failed restore preserves original data.
- Price API TLS, schema and timeout handling; no personal data transmission.

### Android device tests
- Unlock fails without authentication; locks on background/timeout/restart.
- Screenshots/recording and recents preview protected as designed.
- No unexpected permissions; logs contain no sensitive data.
- Offline mode works; phone restart and OS background restrictions do not duplicate investments.
- Release APK signed, verified, reproducible enough for traceability, installed and tested on actual phone.

### MVP release checklist
- [ ] Signed APK installs and launches.
- [ ] SQLCipher and secure key management verified on device.
- [ ] Biometric/device unlock and auto-lock work.
- [ ] Portable encrypted backup restores on a second device.
- [ ] Daily/weekly tasks, XP and streaks work.
- [ ] Mutual funds, stocks, ETFs, EPF and bank balances can be entered manually.
- [ ] Monthly recurring investments require confirmation and never duplicate.
- [ ] Expense categories, transfers and CSV import work.
- [ ] Dashboard and goals display correct, dated figures.
- [ ] All core features work offline.
- [ ] Dependency, permission, logging and security tests pass.

## 11. Initial local development commands

```bash
mkdir lifeos && cd lifeos
git init
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install kivy pytest ruff requests
mkdir -p app/ui app/modules app/data app/security tests docs scripts
code .
```

This sets up a Python development environment **only**. It does not build the APK or configure encryption. Buildozer/android packaging should run in a Linux CI environment; use a physical phone instead of a heavy emulator on an 8 GB Mac.

## 12. Open design decisions

- Final product name, branding and icon (LifeOS is working name).
- Exact Android min/target SDK, Python/Kivy/KivyMD and SQLCipher binding versions after compatibility prototype.
- Price-data provider and availability/licensing for NSE/BSE and mutual fund NAV data.
- Whether liabilities and advanced returns are included in first MVP or subsequent update.
- Whether notifications are needed and their Android permissions.
- Recovery password UX and secure backup destination.
- Whether to introduce optional SMS transaction processing later (not authorized for MVP).

## 13. Engineering principles

Keep finance math independent of UI. Never treat a scheduled SIP as completed. Prefer a reliable local ledger to fragile automation. Treat imported files and API responses as untrusted. Do not over-engineer with microservices or cloud infrastructure. Review all security-sensitive native bridge code. Maintain schema migrations and recovery testing with every release.

---
**Reference status:** This document is a planning specification, not evidence that any feature or security control has been implemented. Revisit and version it as implementation decisions are validated.
