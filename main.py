# === Web Server for Replit ===
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# === Imports ===
import requests
import pandas as pd
import time
import datetime
import ta
from tradingview_ta import TA_Handler, Interval

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Telegram Config ===
TELEGRAM_TOKEN = '8162837839:AAEP8UP7Q1lFIZOIXrvfBsmSAZ16STOO0Ss'
TELEGRAM_CHAT_ID = '941162624'  # for sending alerts outside Telegram handlers

# === Globals ===
symbols = {
    'bitcoin': 'BTC/USDT',
    'solana': 'SOL/USDT',
    'dogwifcoin': 'WIF/USDT'
}
vs_currency = 'usd'
days = 30
rsi_period = 14
trend_ma_period = 20
check_interval = 60 * 5  # 5 minutes

open_trades = {}
closed_trades = []
daily_signals = []

# === Utility Functions ===

def send_telegram(message: str):
    # Send message via Telegram bot API directly (for alerts outside handlers)
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")

# === Telegram Handlers (async) ===

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['Check Bot Status', 'List Open Trades'],
        ['Add New Pair', 'Closed Trades'],
        ['Daily Signals', 'Monthly Trades']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Welcome! Choose an option below or type a command:\n\n"
        "/ping - Check if bot is alive\n"
        "/status - Show open trades\n"
        "/addpair <coin_name_or_symbol> - Add a new trading pair\n"
        "/closedtrades - Show last closed trades and profits\n"
        "/dailysignals - Show signals generated today\n"
        "/monthlytrades - Show this month's trade summary\n\n"
        "Tap a button below to get started.",
        reply_markup=reply_markup
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Bot is alive and running!')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not open_trades:
        await update.message.reply_text("🤖 No open trades at the moment.")
        return

    msg_lines = ["📋 Current Open Trades:"]
    for coin_id, trade in open_trades.items():
        status = trade.get("status", "unknown")
        entry = trade.get("entry", 0)
        sl = trade.get("sl", 0)
        target = trade.get("target", 0)
        direction = trade.get("direction", "N/A")

        line = (f"{coin_id.upper()} — {direction} | Entry: ${entry:.4f} | "
                f"SL: ${sl:.4f} | Target: ${target:.4f} | Status: {status}")
        msg_lines.append(line)

    await update.message.reply_text("\n".join(msg_lines))

async def addpair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /addpair <coin_name_or_symbol>\nExample: /addpair bitcoin")
        return

    query = " ".join(context.args).lower()

    # Fetch coins list from CoinGecko
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        coins = response.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to fetch coins list: {e}")
        return

    matched = None
    for coin in coins:
        if coin['id'].lower() == query or coin['symbol'].lower() == query or coin['name'].lower() == query:
            matched = coin
            break

    if not matched:
        await update.message.reply_text(f"❌ No coin found matching '{query}'. Try coin ID, symbol, or full name.")
        return

    coin_id = matched['id']
    symbol = matched['symbol'].upper()
    pair_label = f"{symbol}/USDT"

    if coin_id in symbols:
        await update.message.reply_text(f"⚠️ Pair for '{coin_id}' already exists.")
        return

    symbols[coin_id] = pair_label
    await update.message.reply_text(f"✅ Added trading pair: {coin_id} → {pair_label}")

async def closedtrades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not closed_trades:
        await update.message.reply_text("🤖 No closed trades yet.")
        return

    msg_lines = ["📈 Closed Trades (Last 10):"]
    total_pnl = 0
    for trade in closed_trades[-10:]:
        coin_id = trade.get("coin", "N/A").upper()
        direction = trade.get("direction", "N/A")
        entry = trade.get("entry", 0)
        exit_price = trade.get("exit_price", 0)
        profit = trade.get("profit", 0)

        line = (f"{coin_id} {direction} | Entry: ${entry:.4f} | Exit: ${exit_price:.4f} | "
                f"P/L: ${profit:.2f}")
        msg_lines.append(line)
        total_pnl += profit

    msg_lines.append(f"\nTotal P/L of last {len(closed_trades[-10:])} trades: ${total_pnl:.2f}")
    await update.message.reply_text("\n".join(msg_lines))

async def dailysignals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not daily_signals:
        await update.message.reply_text("📉 No trade signals generated today yet.")
        return

    msg_lines = ["📊 Signals generated today:"]
    for signal in daily_signals[-20:]:
        line = (f"{signal['time']} — {signal['coin']} {signal['direction']} | Entry: ${signal['entry']:.4f} "
                f"SL: ${signal['sl']:.4f} Target: ${signal['target']:.4f}\nReason: {signal['reason']}")
        msg_lines.append(line)

    await update.message.reply_text("\n\n".join(msg_lines))

async def monthlytrades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    trades_this_month = [
        trade for trade in closed_trades
        if trade.get("exit_time") and
           trade["exit_time"].month == current_month and
           trade["exit_time"].year == current_year
    ]

    if not trades_this_month:
        await update.message.reply_text("📅 No trades closed this month yet.")
        return

    msg_lines = [f"📅 Trades Closed in {now.strftime('%B %Y')}:"]

    total_pnl = 0
    for trade in trades_this_month:
        coin_id = trade.get("coin", "N/A").upper()
        direction = trade.get("direction", "N/A")
        entry = trade.get("entry", 0)
        exit_price = trade.get("exit_price", 0)
        profit = trade.get("profit", 0)

        line = (f"{coin_id} {direction} | Entry: ${entry:.4f} | Exit: ${exit_price:.4f} | "
                f"P/L: ${profit:.2f}")
        msg_lines.append(line)
        total_pnl += profit

    msg_lines.append(f"\nTotal P/L for {now.strftime('%B %Y')}: ${total_pnl:.2f}")
    await update.message.reply_text("\n".join(msg_lines))

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == 'check bot status':
        await update.message.reply_text("✅ Bot is alive and running!")
    elif text == 'list open trades':
        await status(update, context)
    elif text == 'add new pair':
        await update.message.reply_text(
            "To add a new trading pair, send the command:\n\n"
            "/addpair <coin_name_or_symbol>\n\n"
            "Example:\n/addpair bitcoin"
        )
    elif text == 'closed trades':
        await closedtrades(update, context)
    elif text == 'daily signals':
        await dailysignals(update, context)
    elif text == 'monthly trades':
        await monthlytrades(update, context)
    else:
        await update.message.reply_text("Sorry, I didn't understand that. Please use the buttons or commands.")

# === Trading and Analysis Functions ===

def create_trade(symbol, direction, entry):
    capital = 100
    leverage = 1
    sl_buffer = 0.02 * entry
    target_buffer = 0.03 * entry
    return {
        "coin": symbol,
        "entry": entry,
        "sl": round(entry - sl_buffer, 4) if direction == "LONG" else round(entry + sl_buffer, 4),
        "target": round(entry + target_buffer, 4) if direction == "LONG" else round(entry - target_buffer, 4),
        "status": "active",
        "direction": direction,
        "capital": capital,
        "leverage": leverage,
        "entry_time": datetime.datetime.now()
    }

def generate_entry_alert(coin, direction, entry_price, sl_price, target_price, reason, rsi, ema20, trend, capital_used=100, leverage=1):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""🚨 NEW TRADE INITIATED ({direction})
🪙 Pair: {coin.upper()}
📈 Entry: ${entry_price:.4f}
🛡️ Stop Loss: ${sl_price:.4f}
🎯 Target: ${target_price:.4f}
💰 Simulated Capital: ${capital_used} at {leverage}x Leverage
📊 RSI: {rsi:.2f} | EMA20: ${ema20:.4f}
📉 Trend: {trend.upper()}
🧠 Reason: {reason}
🕒 Time: {now}

📍 The bot is now simulating this trade. You will receive updates on breakeven moves, targets, or SL being hit."""

def track_trades(current_price, coin_id):
    if coin_id not in open_trades:
        return

    trade = open_trades[coin_id]
    if trade["status"] != "active":
        return

    entry = trade["entry"]
    target = trade["target"]
    sl = trade["sl"]
    direction = trade["direction"]
    now = datetime.datetime.now()

    profit = 0
    closed = False
    exit_reason = ""
    exit_price = current_price

    if direction == "LONG":
        if current_price >= target:
            profit = (target - entry) * trade["leverage"]
            exit_reason = "Target hit"
            closed = True
        elif current_price <= sl:
            profit = (sl - entry) * trade["leverage"]
            exit_reason = "Stop Loss hit"
            closed = True
        elif current_price >= entry + 0.01 * entry:
            send_telegram(f"🔁 {coin_id.upper()} LONG — Moved SL to breakeven.")
    else:
        if current_price <= target:
            profit = (entry - target) * trade["leverage"]
            exit_reason = "Target hit"
            closed = True
        elif current_price >= sl:
            profit = (entry - sl) * trade["leverage"]
            exit_reason = "Stop Loss hit"
            closed = True
        elif current_price <= entry - 0.01 * entry:
            send_telegram(f"🔁 {coin_id.upper()} SHORT — Moved SL to breakeven.")

    if closed:
        trade["status"] = "closed"
        trade["exit_price"] = exit_price
        trade["exit_time"] = now
        trade["profit"] = round(profit * trade["capital"], 2)
        closed_trades.append(trade)
        del open_trades[coin_id]

        msg = f"🎯 {coin_id.upper()} {direction} — {exit_reason} at ${exit_price:.4f}\n"
        msg += f"💵 Profit/Loss: ${trade['profit']}"
        send_telegram(msg)

def fetch_ohlcv(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency={vs_currency}&days={days}'
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"❌ Error fetching OHLC for {coin_id}: {e}")
        return None

def fetch_tradingview_indicators(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_5_MINUTES
        )
        analysis = handler.get_analysis()
        indicators = analysis.indicators
        return {
            "rsi": indicators.get("RSI"),
            "ema20": indicators.get("EMA20")
        }
    except Exception as e:
        print(f"❌ Error fetching TradingView data for {symbol}: {e}")
        return {"rsi": None, "ema20": None}

def analyze(df, tv_indicators):
    df['sma'] = df['close'].rolling(window=trend_ma_period).mean()
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=rsi_period).rsi()

    latest_close = df['close'].iloc[-1]
    latest_sma = df['sma'].iloc[-1]
    local_rsi = df['rsi'].iloc[-1]

    tv_rsi = tv_indicators["rsi"]
    tv_ema = tv_indicators["ema20"]

    trend = "uptrend" if latest_close > latest_sma else "downtrend"
    signal = None
    reason = ""
    setup = None

    if trend == "downtrend" and tv_rsi and tv_rsi > 70 and latest_close < tv_ema:
        signal = "SHORT"
        reason = "TV RSI overbought + price below EMA20 + bearish trend"
    elif trend == "uptrend" and tv_rsi and tv_rsi < 30 and latest_close > tv_ema:
        signal = "LONG"
        reason = "TV RSI oversold + price above EMA20 + bullish trend"
    elif trend == "downtrend" and tv_rsi and 65 < tv_rsi <= 70:
        setup = "SHORT setup forming — RSI rising into overbought"
    elif trend == "uptrend" and tv_rsi and 30 <= tv_rsi < 35:
        setup = "LONG setup forming — RSI recovering from oversold"

    return {
        "trend": trend,
        "rsi": local_rsi,
        "tv_rsi": tv_rsi,
        "close": latest_close,
        "sma": latest_sma,
        "ema20": tv_ema,
        "signal": signal,
        "reason": reason,
        "setup": setup
    }

# === Main monitoring loop ===
def run_monitoring():
    print(f"🚀 Bot Live — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    send_telegram("🤖 Bot is now running and monitoring the markets.")
    while True:
        for coin_id, label in symbols.items():
            print(f"\n📊 Analyzing {label}...")
            df = fetch_ohlcv(coin_id)
            symbol_name = label.replace('/', '')
            tv_indicators = fetch_tradingview_indicators(symbol_name)

            if df is not None and len(df) > trend_ma_period:
                result = analyze(df, tv_indicators)
                current_price = result["close"]

                print(f"  ➤ Price: {current_price:.4f}")
                print(f"  ➤ RSI (local): {result['rsi']:.2f} | RSI (TV): {result['tv_rsi']}")
                print(f"  ➤ EMA20 (TV): {result['ema20']}")
                print(f"  ➤ Trend: {result['trend']}")

                track_trades(current_price, coin_id)

                if result['signal']:
                    # Only enter a new trade if none active
                    if coin_id not in open_trades or open_trades[coin_id]['status'] != 'active':
                        trade = create_trade(coin_id, result['signal'], current_price)
                        open_trades[coin_id] = trade

                        daily_signals.append({
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "coin": coin_id.upper(),
                            "direction": result['signal'],
                            "entry": current_price,
                            "sl": trade['sl'],
                            "target": trade['target'],
                            "reason": result['reason']
                        })

                        msg = generate_entry_alert(
                            coin=coin_id,
                            direction=result['signal'],
                            entry_price=current_price,
                            sl_price=trade['sl'],
                            target_price=trade['target'],
                            reason=result['reason'],
                            rsi=result['tv_rsi'],
                            ema20=result['ema20'],
                            trend=result['trend']
                        )
                        print(msg)
                        send_telegram(msg)
                elif result['setup']:
                    setup_msg = f"⚠️ {label}: {result['setup']}"
                    print(setup_msg)
                    send_telegram(setup_msg)
                else:
                    print("📉 No trade setup or signal at this time.")
            else:
                print(f"❌ Failed to fetch data for {coin_id}")
        
        print(f"⏰ Waiting {check_interval} seconds before next check...")
        time.sleep(check_interval)

def log_friend_trade(trade_message):
    """Analyze a friend's trade and provide insights"""
    try:
        lines = trade_message.strip().split('\n')
        symbol = lines[0]
        direction = lines[1]
        entry_line = lines[2]
        sl_line = lines[3]
        targets_line = lines[4]
        
        # Extract values
        entry_price = float(entry_line.split(':')[1].strip())
        sl_price = float(sl_line.split(':')[1].strip())
        targets = [float(t.strip()) for t in targets_line.split(':')[1].split(',')]
        
        # Get coin ID from symbol
        coin_id = None
        for cid, sym in symbols.items():
            if sym == symbol:
                coin_id = cid
                break
        
        if not coin_id:
            send_telegram(f"❌ Symbol {symbol} not found in tracked pairs")
            return
        
        # Fetch current data
        df = fetch_ohlcv(coin_id)
        symbol_name = symbol.replace('/', '')
        tv_indicators = fetch_tradingview_indicators(symbol_name)
        
        if df is not None and len(df) > trend_ma_period:
            result = analyze(df, tv_indicators)
            current_price = result["close"]
            
            # Calculate risk/reward
            if direction == "LONG":
                risk = entry_price - sl_price
                reward = targets[0] - entry_price
            else:
                risk = sl_price - entry_price
                reward = entry_price - targets[0]
            
            rr_ratio = reward / risk if risk > 0 else 0
            
            # Generate analysis
            analysis = f"""🔍 Friend Trade Analysis - {symbol}

📊 Trade Details:
• Direction: {direction}
• Entry: ${entry_price:.4f}
• Stop Loss: ${sl_price:.4f}
• Target: ${targets[0]:.4f}
• Risk/Reward: {rr_ratio:.2f}

📈 Current Market:
• Price: ${current_price:.4f}
• RSI: {result['tv_rsi']:.2f} 
• EMA20: ${result['ema20']:.4f}
• Trend: {result['trend'].upper()}

🧠 Analysis:
"""
            
            if direction == "LONG":
                if result['tv_rsi'] < 40 and current_price > result['ema20']:
                    analysis += "✅ GOOD SETUP - RSI supports long, price above EMA20"
                elif result['tv_rsi'] > 60:
                    analysis += "⚠️ RISKY - RSI getting overbought for long position"
                else:
                    analysis += "📊 NEUTRAL - Mixed signals, manage risk carefully"
            else:
                if result['tv_rsi'] > 60 and current_price < result['ema20']:
                    analysis += "✅ GOOD SETUP - RSI supports short, price below EMA20"
                elif result['tv_rsi'] < 40:
                    analysis += "⚠️ RISKY - RSI getting oversold for short position"
                else:
                    analysis += "📊 NEUTRAL - Mixed signals, manage risk carefully"
            
            print(analysis)
            send_telegram(analysis)
        else:
            send_telegram(f"❌ Could not fetch market data for {symbol}")
            
    except Exception as e:
        send_telegram(f"❌ Friend trade analysis failed: {str(e)}")
        print(f"❌ Friend trade analysis failed: {str(e)}")

# === Main Execution ===
if __name__ == "__main__":
    # Start web server for Replit
    keep_alive()
    
    # Start Telegram bot
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start_command))
    app_bot.add_handler(CommandHandler("ping", ping))
    app_bot.add_handler(CommandHandler("status", status))
    app_bot.add_handler(CommandHandler("addpair", addpair))
    app_bot.add_handler(CommandHandler("closedtrades", closedtrades))
    app_bot.add_handler(CommandHandler("dailysignals", dailysignals))
    app_bot.add_handler(CommandHandler("monthlytrades", monthlytrades))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    
    # Start monitoring in background
    monitor_thread = Thread(target=run_monitoring)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Start bot
    print("🤖 Starting Telegram bot...")
    app_bot.run_polling()