from config.settings import MIN_RISK_REWARD_RATIO, MIN_CONFIDENCE_SCORE

def check_risk_reward(signal):
    try:
        entry = float(signal["entry"])
        stop = float(signal["stop_loss"])
        target = float(signal["target"])

        if signal["direction"].lower() == "long":
            risk = entry - stop
            reward = target - entry
        else:
            risk = stop - entry
            reward = entry - target

        if risk <= 0:
            return False

        rr = reward / risk
        return rr >= MIN_RISK_REWARD_RATIO

    except Exception as e:
        print(f"Risk/reward check error: {e}")
        return False


def filter_by_confidence(score):
    return score >= MIN_CONFIDENCE_SCORE
