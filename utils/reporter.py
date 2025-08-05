import os
import json
from datetime import datetime

def generate_report_files(scored, target_url):
    os.makedirs("results", exist_ok=True)

    # Save data for streamlit
    with open("results/final_report_data.json", "w") as f:
        json.dump({
            "target": target_url,
            "scored": scored
        }, f, indent=2)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = len(scored)
    high = sum(1 for s in scored if s["risk"] == "High")
    medium = sum(1 for s in scored if s["risk"] == "Medium")
    low = total - high - medium

    # Scoring Criteria
    scoring_criteria = "<ul>"
    if high:
        scoring_criteria += "<li><b>High</b>: Sensitive paths like <code>/admin</code>, <code>/login</code>, or tokens in URL.</li>"
    if medium:
        scoring_criteria += "<li><b>Medium</b>: Backup folders or dev routes like <code>/config/</code>, <code>/test/</code>.</li>"
    if low:
        scoring_criteria += "<li><b>Low</b>: Static pages, assets or public resources.</li>"
    scoring_criteria += "</ul>"

    # Recommendations
    recommendations = "<ul>"
    if high:
        recommendations += "<li>Use authentication and rate-limiting for sensitive endpoints.</li>"
        recommendations += "<li>Avoid exposing tokens or credentials in URL params.</li>"
    if medium:
        recommendations += "<li>Remove or secure old/dev/config folders.</li>"
    recommendations += "<li>Regularly audit URLs for exposure.</li>"
    recommendations += "<li>Enable logging for endpoint access.</li>"
    recommendations += "</ul>"

    # Conclusion
    if high:
        conclusion = f"<b>{high}</b> high-risk endpoints detected. Immediate action recommended."
    elif medium:
        conclusion = f"<b>{medium}</b> medium-risk endpoints found. Review access controls."
    else:
        conclusion = "No critical risks found. Target appears secure."

    # HTML Table Rows with S.No. and risk color coding
    rows = ""
    for idx, item in enumerate(scored, start=1):
        color = "#ff4d4d" if item["risk"] == "High" else "#ffa500" if item["risk"] == "Medium" else "#5cb85c"
        rows += f"""
        <tr style="background-color:{color}22;">
            <td>{idx}</td>
            <td><code>{item['url']}</code></td>
            <td><b style="color:{color};">{item['risk']}</b></td>
            <td>{item['reason']}</td>
        </tr>
        """

    # Full HTML
    html_content = f"""
    <html>
    <head>
        <title>ShadowLink Report - {target_url}</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #f4f4f4;
                color: #222;
                padding: 20px;
            }}
            h1, h2 {{
                color: #003366;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #003366;
                color: white;
            }}
            code {{
                color: #c7254e;
                background-color: #f9f2f4;
                padding: 2px 4px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <h1>🔍 ShadowLink Vulnerability Report</h1>
        <p><b>Scan Time:</b> {now}</p>
        <p><b>Target:</b> {target_url}</p>

        <h2>📋 Discovered Endpoints</h2>
        <table>
            <tr>
                <th>S.No.</th>
                <th>Endpoint</th>
                <th>Risk</th>
                <th>Reason</th>
            </tr>
            {rows}
        </table>

        <h2>📊 Scoring Criteria</h2>
        {scoring_criteria}

        <h2>🧾 Recommendations</h2>
        {recommendations}

        <h2>📌 Conclusion</h2>
        <p>{conclusion}</p>
    </body>
    </html>
    """

    with open("results/final_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
