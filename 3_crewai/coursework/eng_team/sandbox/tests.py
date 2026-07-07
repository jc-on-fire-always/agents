
import unittest
from backend import TradingAccount, get_share_price

class TestTradingSystem(unittest.TestCase):
    def setUp(self):
        self.account = TradingAccount(1000.0)

    def test_deposit_and_withdraw(self):
        self.assertTrue(self.account.deposit(500.0))
        self.assertEqual(self.account.balance, 1500.0)
        self.assertTrue(self.account.withdraw(200.0))
        self.assertEqual(self.account.balance, 1300.0)
        self.assertFalse(self.account.withdraw(2000.0)) # Insufficient funds
        self.assertEqual(self.account.balance, 1300.0)

    def test_trade_execution(self):
        # Buy shares
        self.assertTrue(self.account.execute_trade("AAPL", 2, True)) # Cost 300
        self.assertEqual(self.account.holdings["AAPL"], 2)
        self.assertEqual(self.account.balance, 700.0)
        
        # Insufficient funds to buy
        self.assertFalse(self.account.execute_trade("GOOGL", 1, True))
        
        # Sell shares
        self.assertTrue(self.account.execute_trade("AAPL", 1, False)) # Revenue 150
        self.assertEqual(self.account.holdings["AAPL"], 1)
        self.assertEqual(self.account.balance, 850.0)
        
        # Insufficient shares to sell
        self.assertFalse(self.account.execute_trade("AAPL", 5, False))

    def test_pnl_calculation(self):
        # Start: 1000
        # Buy 1 AAPL (150) -> Balance 850, Holding: 1 AAPL (150) -> Total: 1000, PnL: 0
        self.account.execute_trade("AAPL", 1, True)
        self.assertEqual(self.account.get_profit_loss(), 0.0)
        
        # Sell 1 AAPL (150) -> Balance 1000, Holding: 0 -> Total: 1000, PnL: 0
        self.account.execute_trade("AAPL", 1, False)
        self.assertEqual(self.account.get_profit_loss(), 0.0)

    def test_transaction_history(self):
        self.account.deposit(100.0)
        self.account.execute_trade("TSLA", 1, True)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["type"], "deposit")
        self.assertEqual(transactions[1]["type"], "buy")

if __name__ == "__main__":
    unittest.main()
