import time
from core.signal_handler import handle_signal
from core.trade_manager import check_open_trades
from utils.telegram import send_telegram_alert

def main():
    send_telegram_alert("🤖 Sniper Bot Live and Monitoring...")
    while True:
        check_open_trades()
        time.sleep(10)

if __name__ == "__main__":
    main()
