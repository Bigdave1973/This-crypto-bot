# pairs.py

import json
from config import PAIRS_PATH

def load_pairs():
    try:
        with open(PAIRS_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_pairs(pairs):
    with open(PAIRS_PATH, "w") as f:
        json.dump(sorted(list(set(pairs))), f, indent=2)

def add_pair(pair):
    pairs = load_pairs()
    pair = pair.upper()
    if pair not in pairs:
        pairs.append(pair)
        save_pairs(pairs)
        return True
    return False

def remove_pair(pair):
    pairs = load_pairs()
    pair = pair.upper()
    if pair in pairs:
        pairs.remove(pair)
        save_pairs(pairs)
        return True
    return False
