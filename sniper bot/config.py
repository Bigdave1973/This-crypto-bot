# config.py

# Telegram
BOT_TOKEN = "8162837839:AAEP8UP7Q1lFIZOIXrvfBsmSAZ16STOO0Ss"
CHAT_ID = 941162624

# Trading simulation settings
DEFAULT_CAPITAL = 100.0  # USD per trade
DEFAULT_LEVERAGE = 5
SLIPPAGE_PERCENT = 0.05  # 0.05% slippage
TRAILING_STOP_TRIGGER = 1.5  # % price move before trailing SL activates

# Paths
TRADE_MEMORY_PATH = "data/trade_memory.json"
PAIRS_PATH = "data/pairs.json"
