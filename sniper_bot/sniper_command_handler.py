# sniper_command_handler.py

from trade_engine import analyze_trade
from open_trade_tracker import OPEN_TRADES
from trade_memory import update_trade_memory
from telegram_alert import send_telegram_alert

def handle_sniper_command(command_text, send_response):
    parts = command_text.strip().split()

    if len(parts) == 0:
        return

    if parts[0] == "/sniper":
        if len(parts) >= 2:
            cmd = parts[1]

            # /sniper open_trades
            if cmd == "open_trades":
                if not OPEN_TRADES:
                    send_response("📭 No open trades right now.")
                else:
                    msg = f"🟡 OPEN TRADES ({len(OPEN_TRADES)})\n\n"
                    for t in OPEN_TRADES:
                        msg += (
                            f"{t['pair']} | {t['direction']} | Entry: {t['entry']}\n"
                            f"SL: {t['sl']} | TP: {t['tp']} | R:R: {t['rr']} | Conf: {t['confidence']}%\n"
                            f"Status: {t['status']}\n\n"
                        )
                    send_response(msg)

            # /sniper analyze BTC/USDT LONG 29800 29400 31000
            elif cmd == "analyze" and len(parts) == 7:
                symbol = parts[2]
                direction = parts[3].upper()
                try:
                    entry = float(parts[4])
                    sl = float(parts[5])
                    tp = float(parts[6])
                except ValueError:
                    return send_response("❌ Invalid price values.")

                data = {
                    "symbol": symbol,
                    "entry": entry,
                    "sl": sl,
                    "tp": tp,
                    "direction": direction
                }

                # Analyze it like a sniper
                decision = analyze_trade(data, is_manual=True)

                if decision["valid"]:
                    decision.update({
                        "pair": symbol,
                        "direction": direction,
                        "entry": entry,
                        "sl": sl,
                        "tp": tp,
                        "status": "open",
                        "is_meme": decision.get("is_meme", False)
                    })
                    update_trade_memory(decision)
                    send_telegram_alert(decision, stage="confirmed")
                    send_response(f"✅ Trade accepted and simulated for {symbol}.")
                else:
                    msg = (
                        f"🚫 TRADE REJECTED: {symbol} | {direction}\n"
                        f"Confidence: {decision['confidence']}%\n"
                        f"R:R: {decision['rr']}\n"
                        f"Reason: {decision['reason']}\n"
                    )
                    send_response(msg)

            else:
                send_response("❓ Unknown /sniper command.")
