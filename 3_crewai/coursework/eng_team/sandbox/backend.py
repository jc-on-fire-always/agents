
def get_share_price(symbol: str) -> float:
    prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2800.0}
    return prices.get(symbol.upper(), 0.0)

class TradingAccount:
    def __init__(self, initial_deposit: float):
        self.initial_deposit = float(initial_deposit)
        self.balance = float(initial_deposit)
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount, "balance": self.balance})
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transactions.append({"type": "withdraw", "amount": amount, "balance": self.balance})
        return True

    def execute_trade(self, symbol: str, quantity: int, is_buy: bool) -> bool:
        if quantity <= 0:
            return False
        
        price = get_share_price(symbol)
        if price == 0:
            return False
        
        cost = price * quantity
        
        if is_buy:
            if self.balance < cost:
                return False
            self.balance -= cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        else:
            if self.holdings.get(symbol, 0) < quantity:
                return False
            self.balance += cost
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
        
        self.transactions.append({
            "type": "buy" if is_buy else "sell",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total": cost
        })
        return True

    def get_portfolio_value(self) -> float:
        stock_value = sum(get_share_price(sym) * qty for sym, qty in self.holdings.items())
        return self.balance + stock_value

    def get_profit_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict[str, int]:
        return self.holdings

    def get_transactions(self) -> list[dict]:
        return self.transactions
