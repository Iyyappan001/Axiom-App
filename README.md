# LifeOS

LifeOS is an Android-only, offline-first personal operating system built with Python and Kivy. It keeps productivity and financial records in an encrypted on-device database; market data is optional and never receives private holdings.

## Status

Planning and foundation scaffold. Do not enter real financial data until the feasibility gates in [`plan/LifeOS_Master_Blueprint.md`](plan/LifeOS_Master_Blueprint.md) pass on physical Android hardware.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
ruff check .
```

The target architecture is `ui -> application services -> domain -> repositories -> encrypted database`, with Android and market-data integrations kept behind adapters.
