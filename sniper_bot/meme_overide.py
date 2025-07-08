# meme_override.py

import json
import os

OVERRIDE_FILE = "config/meme_overrides.json"

def load_overrides():
    if not os.path.exists(OVERRIDE_FILE):
        return {"marked": [], "unmarked": []}
    with open(OVERRIDE_FILE, "r") as f:
        return json.load(f)

def save_overrides(data):
    with open(OVERRIDE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def mark_meme(pair):
    data = load_overrides()
    if pair not in data["marked"]:
        data["marked"].append(pair)
    if pair in data["unmarked"]:
        data["unmarked"].remove(pair)
    save_overrides(data)
    return f"✅ Marked {pair} as a MEME coin."

def unmark_meme(pair):
    data = load_overrides()
    if pair not in data["unmarked"]:
        data["unmarked"].append(pair)
    if pair in data["marked"]:
        data["marked"].remove(pair)
    save_overrides(data)
    return f"✅ Unmarked {pair} from meme coin list."

def is_meme_coin(pair):
    # Built-in list
    known_memes = {"PEPE", "WIF", "DOGWIFCOIN", "TURBO", "SHIBA", "FLOKI", "MONG"}

    data = load_overrides()
    base = pair.replace("/USDT", "").upper()

    # Manual override takes priority
    if base in data["marked"]:
        return True
    if base in data["unmarked"]:
        return False

    return base in known_memes
