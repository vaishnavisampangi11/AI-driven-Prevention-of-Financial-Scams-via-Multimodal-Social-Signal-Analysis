def decide_action(risk_score):
    if risk_score <= 30:
        return {
            "decision": "ALLOW",
            "action": "Proceed with caution; no major suspicious indicators were found.",
            "reason": "The risk score is low and does not exceed the suspicious threshold.",
        }
    if risk_score <= 60:
        return {
            "decision": "WARN",
            "action": "Verify the sender or link before continuing.",
            "reason": "Suspicious patterns were detected and the user should confirm the source.",
        }
    if risk_score <= 80:
        return {
            "decision": "RESTRICT",
            "action": "Do not proceed until the communication is independently verified.",
            "reason": "The content shows several strong scam indicators and a high-risk profile.",
        }
    return {
        "decision": "BLOCK",
        "action": "Stop interaction immediately and avoid sharing any OTP, password, or payment information.",
        "reason": "Critical scam indicators were detected and the interaction should be halted.",
    }
