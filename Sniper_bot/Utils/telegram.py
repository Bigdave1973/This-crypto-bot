def send_telegram_alert(msg):
    print("[Telegram]", msg)

def send_trade_alert(trade, source="Bot"):
    print(f"🚨 NEW TRADE from {source}\\nPair: {trade['pair']} | Direction: {trade['direction']} | Entry: {trade['entry_price']}\\nConfidence: {trade['confidence']} | Risk: {trade['risk_level']}")

def send_rejection_alert(signal, reasons):
    print(f"❌ TRADE REJECTED: {signal['pair']} | Reason(s): {', '.join(reasons)}")

def send_trade_exit_alert(pair, exit_price, result, pnl):
    print(f"✅ TRADE CLOSED\\nPair: {pair} | Exit: {exit_price} | Result: {result} | PnL: ${pnl:.2f}")
