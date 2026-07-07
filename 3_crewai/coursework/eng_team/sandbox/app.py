import gradio as gr
from backend import TradingAccount

def handle_deposit(account: TradingAccount, amount: float) -> tuple[float, str]:
    if account.deposit(amount):
        return account.balance, "Success"
    return account.balance, "Failed"

def handle_withdraw(account: TradingAccount, amount: float) -> tuple[float, str]:
    if account.withdraw(amount):
        return account.balance, "Success"
    return account.balance, "Failed"

def handle_trade(account: TradingAccount, symbol: str, qty: int, is_buy: bool) -> tuple[str, float, float, dict, list]:
    success = account.execute_trade(symbol, qty, is_buy)
    msg = "Success" if success else "Failed"
    return msg, account.balance, account.get_profit_loss(), account.get_holdings(), account.get_transactions()

with gr.Blocks() as demo:
    account = gr.State(TradingAccount(1000.0))
    
    gr.Markdown("# Trading Simulation")
    
    with gr.Row():
        balance_display = gr.Number(value=1000.0, label="Balance", interactive=False)
        pnl_display = gr.Number(value=0.0, label="PnL", interactive=False)
        
    with gr.Tab("Deposit/Withdraw"):
        amount_input = gr.Number(label="Amount")
        dep_btn = gr.Button("Deposit")
        wit_btn = gr.Button("Withdraw")
        status_out = gr.Textbox(label="Status")
        
    with gr.Tab("Trade"):
        symbol_input = gr.Dropdown(["AAPL", "TSLA", "GOOGL"], label="Symbol")
        qty_input = gr.Number(label="Quantity", value=1)
        buy_btn = gr.Button("Buy")
        sell_btn = gr.Button("Sell")
        trade_status = gr.Textbox(label="Trade Status")
        
    with gr.Tab("Portfolio"):
        holdings_display = gr.JSON(label="Holdings")
        transactions_display = gr.JSON(label="Transactions")

    # Bindings
    dep_btn.click(handle_deposit, [account, amount_input], [balance_display, status_out])
    wit_btn.click(handle_withdraw, [account, amount_input], [balance_display, status_out])
    
    buy_btn.click(handle_trade, [account, symbol_input, qty_input, gr.State(True)], 
                  [trade_status, balance_display, pnl_display, holdings_display, transactions_display])
    sell_btn.click(handle_trade, [account, symbol_input, qty_input, gr.State(False)], 
                   [trade_status, balance_display, pnl_display, holdings_display, transactions_display])

if __name__ == "__main__":
    demo.launch()
