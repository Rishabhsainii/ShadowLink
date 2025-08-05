import streamlit as st
import subprocess
import json
import time
import os
import atexit

st.set_page_config(page_title="ShadowLink Dashboard", layout="wide")
st.title("🕵️ ShadowLink Dashboard")

target = st.text_input("🔗 Enter target URL:", placeholder="e.g. http://example.com")
col1, col2 = st.columns(2)

# ========== 🚀 Run Scanner ==========
if col1.button("🚀 Run Scan"):
    st.info(f"Running scanner for: {target}")
    
    if not target.startswith("http"):
        st.error("❌ Invalid URL. Please enter full URL starting with http:// or https://")
    else:
        with st.spinner("🔎 Scanning target, please wait..."):
            result = subprocess.run(
                ["python", "scanner.py", target],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                st.success("✅ Scan complete.")
                st.code(result.stdout)
            else:
                st.error("❌ Scan failed.")
                st.code(result.stderr)

# ========== 🔁 Refresh Data ==========
if col2.button("🔁 Refresh Data"):
    if os.path.exists("results/final_report_data.json"):
        with open("results/final_report_data.json", "r") as f:
            data = json.load(f)

        scored = data["scored"]
        target = data["target"]

        st.subheader(f"📄 Report for {target}")
        st.write(f"Total endpoints: {len(scored)}")

        # Risk chart
        st.markdown("### 🔍 Risk Distribution")
        risk_count = {"High": 0, "Medium": 0, "Low": 0}
        for i in scored:
            risk_count[i["risk"]] += 1
        st.bar_chart(risk_count)

        # Endpoint Table
        st.markdown("### 📋 Scanned Endpoints")
        st.dataframe(scored, use_container_width=True)

        # 🧾 HTML Preview + Download
        if os.path.exists("results/final_report.html"):
            with open("results/final_report.html", "r", encoding="utf-8") as f:
                html = f.read()

            st.markdown("### 🧾 Final Report Preview")
            st.components.v1.html(html, height=600, scrolling=True)

            st.download_button("⬇️ Download Full Report (HTML)", html, file_name="shadowlink_report.html", mime="text/html")
        else:
            st.warning("⚠️ HTML report not found. Run scan again.")
    else:
        st.warning("⚠️ Report file not found. Run scan first.")

# ========== 🧹 Cleanup on Exit ==========
def cleanup_files():
    temp_files = [
        "results/raw_page.html",
        "results/extracted_links.txt",
        "results/all_discovered_links.txt",
        "results/scored_endpoints.txt"
    ]
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"[🧹] Deleted temporary file: {file}")
            except Exception as e:
                print(f"[!] Error deleting {file}: {e}")

atexit.register(cleanup_files)
