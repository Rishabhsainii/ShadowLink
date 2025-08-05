# 🕵️ ShadowLink 

**ShadowLink** is a modern web reconnaissance tool designed to discover and analyze hidden, sensitive, and potentially risky endpoints in any web application.  
It uses a hybrid approach of HTML/JS parsing, robots.txt/sitemap analysis, and smart scoring — and is ready to integrate AI for attack surface prediction.

---

## 🚨 Why ShadowLink?

Most scanners only look for known paths or basic HTML links.  
But real-world attackers use patterns, naming logic, and guessable endpoints to find hidden attack surfaces.

ShadowLink tries to **simulate that mindset** with:
- Static analysis + heuristic scoring
- Optional AI logic
- Detailed reporting (HTML + dashboard)

---

## 🔍 Features

| Feature                                      | Status       |
|---------------------------------------------|--------------|
| Extracts links from HTML & JS               | ✅ Done       |
| Parses `robots.txt` and `sitemap.xml`       | ✅ Done       |
| Scores endpoints based on risk heuristics   | ✅ Done       |
| Generates professional HTML reports         | ✅ Done       |
| Streamlit dashboard for visualization       | ✅ Done       |
| Auto-cleans temp files on exit              | ✅ Done       |
| HTTPS support                               | ✅ Done       |

---

## 🚀 Installation & Setup

### 1. Clone the repository

1
git clone https://github.com/Rishabhsainii/ShadowLink
cd shadowlink

2 Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

3 Install dependencies
pip install -r requirements.txt

4 Usage

CLI Mode (Direct Terminal)
python scanner.py https://example.com

GUI Mode (Streamlit Dashboard)
streamlit run streamlit_app.py

Output Files
| File                              | Description                           |
| --------------------------------- | ------------------------------------- |
| `results/final_report.html`       | Full HTML report with risk highlights |
| `results/final_report_data.json`  | Structured JSON for GUI/reporting     |
| Temp files (auto-deleted on exit) | Includes HTML source and raw links    |

Scoring Criteria
| Risk Level | Description                               |
| ---------- | ----------------------------------------- |
| High       | Endpoints likely sensitive (e.g., /admin) |
| Medium     | Dev/test paths, old versions              |
| Low        | Public links, static or safe              |

Auto-Cleanup
On exit (Ctrl + C or Streamlit shutdown), ShadowLink cleans up:
-raw_page.html
-extracted_links.txt
-all_discovered_links.txt
-scored_endpoints.txt
Only final reports are preserved

Author
Rishabh Saini
