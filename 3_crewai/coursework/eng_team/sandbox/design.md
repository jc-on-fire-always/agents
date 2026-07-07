# Design Document: Trading Simulation Account Management System

## 1. Overview
This system is an account management backend and Gradio interface designed to track user funds, share holdings, and trade history for a trading simulation. It ensures transactional integrity (no negative balances, no overselling/overbuying).

## 2. Module Structure
All code will reside in the root directory:
* `backend.py`: Core logic, state management, and financial calculations.
* `app.py`: Gradio 6.x interface definition.
* `tests.py`: Unit tests for `backend.py`.

---

## 3. Engineering Assignments

### Backend Engineer (`backend.py`)
Responsible for implementing the core `TradingAccount` class and the `get_share_price` mock.

**Functions/Methods:**
* `get_share_price(symbol: str) -> float`: Returns current mock price.
* `class TradingAccount`:
    * `__init__(self, initial_deposit: float)`
    * `deposit(self, amount: float) -> bool`
    * `withdraw(self, amount: float) -> bool`: Prevent if `balance < amount`.
    * `execute_trade(self, symbol: str, quantity: int, is_buy: bool) -> bool`:
        * Logic: Calculate cost/revenue, check balance/holdings, update `balance` and `holdings` dict, record transaction.
    * `get_portfolio_value() -> float`: Sum of `balance` + (sum of `quantity * current_price`).
    * `get_profit_loss() -> float`: `current_portfolio_value - initial_deposit`.
    * `get_holdings() -> dict[str, int]`
    * `get_transactions() -> list[dict]`

### Frontend Engineer (`app.py`)
Responsible for the Gradio 6.x UI. 
*Note: Use Gradio 6 patterns: use `gr.Blocks()` as the main container. Ensure event handlers explicitly map inputs to outputs. Use `gr.State` for managing the `TradingAccount` instance across user sessions.*

**Key Components:**
* `gr.Number` for deposit/withdraw/trade quantity inputs.
* `gr.Dropdown` for share symbols (AAPL, TSLA, GOOGL).
* `gr.Dataframe` or `gr.Markdown` for holdings and transaction history tables.
* `gr.Plot` or `gr.Label` for PnL and total value display.

**Gradio 6 Guidance:**
* Always bind event triggers (e.g., `.click()`) to functions that return values for the output components.
* Use `gr.State` to store the active `TradingAccount` object; pass it as the first argument in event functions.
* When updating multiple components, return a dictionary of `{component: new_value}` or a tuple matching the order of output components defined in the event trigger.

### Test Engineer (`tests.py`)
Responsible for `unittest` suite covering:
* `test_deposit_and_withdraw`: Verify math and balance constraints.
* `test_trade_execution`: Verify buy/sell validation (insufficient funds, insufficient shares).
* `test_portfolio_calculations`: Verify PnL and total value accuracy with mock prices.
* `test_transaction_history`: Ensure every action is logged correctly.

---

## 4. Class & Signature Specifications

### `backend.py`
```python
def get_share_price(symbol: str) -> float: ...

class TradingAccount:
    def __init__(self, initial_deposit: float): ...
    def deposit(self, amount: float) -> bool: ...
    def withdraw(self, amount: float) -> bool: ...
    def execute_trade(self, symbol: str, quantity: int, is_buy: bool) -> bool: ...
    def get_portfolio_value(self) -> float: ...
    def get_profit_loss(self) -> float: ...
    def get_holdings(self) -> dict[str, int]: ...
    def get_transactions(self) -> list[dict]: ...
```

### `app.py`
```python
# Event Handlers
def handle_deposit(account: TradingAccount, amount: float) -> tuple[float, str]: ...
def handle_trade(account: TradingAccount, symbol: str, qty: int, is_buy: bool) -> tuple[str, float, float]: ...
# Main entry point using gr.Blocks()
```

### `tests.py`
```python
import unittest
class TestTradingSystem(unittest.TestCase):
    def test_insufficient_funds_buy(self): ...
    def test_insufficient_shares_sell(self): ...
    def test_pnl_calculation(self): ...
```