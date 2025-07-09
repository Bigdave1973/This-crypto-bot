# utils.py

import json
import os

MEME_COIN_LIST = [
    "DOGWIFCOIN", "PEPE", "WIF", "SHIB", "FLOKI", "DOGE", "LADYS", "ELON",
    "JEFF", "BORK", "PITBULL", "HARRY", "BONK", "MOG", "PONKE", "TURBO"
]

MEME_OVERRIDE_PATH = "data/meme_overrides.json"

# Ensure the override file exists
def _load_meme_overrides():
    if not os.path.exists(MEME_OVERRIDE_PATH):
        with open(MEME_OVERRIDE_PATH, "w") as f:
            json.dump({"force_meme": [], "force_normal": []}, f)

    with open(MEME_OVERRIDE_PATH, "r") as f:
        return json.load(f)

def _save_meme_overrides(data):
    with open(MEME_OVERRIDE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def is_meme_coin(symbol: str) -> bool:
    symbol = symbol.upper().replace("USDT", "")
    overrides = _load_meme_overrides()

    if symbol in overrides["force_normal"]:
        return False
    if symbol in overrides["force_meme"]:
        return True
    return symbol in MEME_COIN_LIST

def mark_meme(symbol: str):
    data = _load_meme_overrides()
    symbol = symbol.upper()
    if symbol not in data["force_meme"]:
        data["force_meme"].append(symbol)
    if symbol in data["force_normal"]:
        data["force_normal"].remove(symbol)
    _save_meme_overrides(data)

def unmark_meme(symbol: str):
    data = _load_meme_overrides()
    symbol = symbol.upper()
    if symbol not in data["force_normal"]:
        data["force_normal"].append(symbol)
    if symbol in data["force_meme"]:
        data["force_meme"].remove(symbol)
    _save_meme_overrides(data)
