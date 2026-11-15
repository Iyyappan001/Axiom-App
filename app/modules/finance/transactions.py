"""Transaction primitives; balances must be derived from confirmed entries."""

from dataclasses import dataclass
from decimal import Decimal
from datetime import date


@dataclass(frozen=True)
class InvestmentTransaction:
    asset_id: str
    account_id: str
    trade_date: date
    transaction_type: str
    units: Decimal
    price: Decimal
    amount: Decimal
    confirmed: bool = False
