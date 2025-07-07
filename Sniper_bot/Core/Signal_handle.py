from utils.memory import save_open_trade
from utils.analysis import analyze_market, score_trade_confidence, validate_trade_risk_reward
from utils.telegram import send_trade_alert, send_rejection_alert
from utils.trade_executor import simulate_trade_execution

def handle_signal(signal):
    market_data = analyze_market(signal["pair"])
    confidence = score_trade_confidence(signal, market_data)
    rr_valid = validate_trade_risk_reward(signal)
    retracement_ok = market_data.get("retracement_zone", False)

    reasons = []
    if confidence < 60:
        reasons.append("Low confidence score")
    if not rr_valid:
        reasons.append("Poor risk-reward ratio")
    if not retracement_ok:
        reasons.append("No valid retracement entry")

    if reasons:
        send_rejection_alert(signal, reasons)
        return

    trade = simulate_trade_execution(signal, confidence)
    save_open_trade(trade)
    send_trade_alert(trade, source=signal.get("source", "Bot"))
