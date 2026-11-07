from pathlib import Path


def build_report_html(analysis_record, detection_records, alerts):
    evidence = "<br>".join(f"- {item}" for item in detection_records)
    alert_lines = "<br>".join(f"- {alert.message}" for alert in alerts)
    html = f"""
    <html>
      <head><title>Scam Analysis Report</title></head>
      <body>
        <h1>Financial Scam Prevention Report</h1>
        <p><strong>Input Type:</strong> {analysis_record.input_type}</p>
        <p><strong>Classification:</strong> {analysis_record.classification}</p>
        <p><strong>Risk Score:</strong> {analysis_record.risk_score}</p>
        <p><strong>Risk Level:</strong> {analysis_record.risk_level}</p>
        <p><strong>Decision:</strong> {analysis_record.decision}</p>
        <p><strong>Recommendation:</strong> {analysis_record.recommendation}</p>
        <h2>Evidence</h2>
        <p>{evidence}</p>
        <h2>Alerts</h2>
        <p>{alert_lines}</p>
      </body>
    </html>
    """
    return html
