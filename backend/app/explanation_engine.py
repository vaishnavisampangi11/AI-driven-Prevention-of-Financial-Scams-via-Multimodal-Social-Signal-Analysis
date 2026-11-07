def build_explanation(detected_type, signals, context=None):
    evidence = []
    if detected_type == "text":
        suspicious_keywords = signals.get("keywords", [])
        if suspicious_keywords:
            evidence.append(f"Urgency cues detected: {', '.join(suspicious_keywords[:3])}")
        if signals.get("financial_request"):
            evidence.append("Financial request detected.")
        if signals.get("impersonation"):
            evidence.append("Potential impersonation or spoofing pattern detected.")
        if not evidence:
            evidence.append("Text contains no strong suspicious signal, but the model still evaluated risk.")
        summary = "The message was evaluated using the trained scam detection model and suspicious linguistic cues."
    elif detected_type == "url":
        features = signals.get("features", {})
        if features.get("url_length") and features["url_length"] > 75:
            evidence.append("URL is unusually long for a normal trusted website.")
        if features.get("subdomain_count", 0) >= 2:
            evidence.append("Multiple subdomains are present.")
        if features.get("is_ip_host"):
            evidence.append("The hostname appears to be an IP address.")
        if features.get("https") is False:
            evidence.append("The URL does not use HTTPS.")
        if features.get("special_chars"):
            evidence.append("Suspicious special characters were detected in the URL structure.")
        if not evidence:
            evidence.append("URL did not match common phishing indicators in the static feature model.")
        summary = "The website address was assessed using URL lexical and structural features to estimate phishing risk."
    else:
        evidence.append("QR content was decoded and assessed for risk.")
        if signals.get("url_risk") is not None:
            evidence.append("Decoded URL was passed to the phishing detector for evaluation.")
        summary = "The QR content was checked for embedded content and relevant risk signals."

    return {
        "summary": summary,
        "evidence": evidence,
    }
