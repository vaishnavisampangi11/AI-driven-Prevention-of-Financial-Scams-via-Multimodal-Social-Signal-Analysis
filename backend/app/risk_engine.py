def calculate_risk_score(signals):
    weights = {
        "text": 0.45,
        "url": 0.35,
        "qr": 0.20,
    }
    score = 0.0
    total_weight = 0.0
    for name, value in signals.items():
        if value is None:
            continue
        score += value * weights.get(name, 0.2)
        total_weight += weights.get(name, 0.2)
    if total_weight == 0:
        return 0
    return min(100, max(0, round(score / total_weight, 2)))


def risk_level(score):
    if score <= 30:
        return "SAFE"
    if score <= 60:
        return "SUSPICIOUS"
    if score <= 80:
        return "HIGH RISK"
    return "CRITICAL"
