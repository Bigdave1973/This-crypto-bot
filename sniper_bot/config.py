# config.py

CONFIG = {
    "pairs": [
        "BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGWIFCOINUSDT", "PEPEUSDT", "WIFUSDT"
    ],

    "meme_coins": [
        "DOGWIFCOIN", "PEPE", "WIF"
    ],

    "scan_interval": 30,  # seconds

    "risk": {
        "default_risk_per_trade": 0.01,
        "meme_trade_min_confidence": 80,
        "min_rr": 1.5,
        "meme_rr": 1.8
    },

    "telegram": {
        "enabled": True,
        "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
        "chat_id": "YOUR_TELEGRAM_CHAT_ID"
    },

    "webhook": {
        "enabled": True,
        "secret": "your_webhook_secret"
    },

    "exchange": {
        "source": "binance",  # Placeholder: assumes Binance-style tickers
        "leverage": 1,
        "simulated_capital": 100
    }
}
