# scanner.py

import argparse
import requests
import os

from parser.html_parser import extract_links_and_scripts
from parser.robots_parser import scan_robots_txt, scan_sitemap
from utils.scorer import score_url_reason
from utils.reporter import generate_report_files


def fetch_html(target_url):
    try:
        print(f"[+] Fetching HTML content from {target_url} ...")
        headers = {"User-Agent": "ShadowLinkScanner/1.0"}
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text, response.headers, response.status_code
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching URL: {e}")
        return None, {}, None


def save_html(content, output_path="results/raw_page.html"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Saved HTML content to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="ShadowLink - Hidden Endpoint Scanner")
    parser.add_argument("url", help="Target website URL (e.g., https://example.com)")
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)

    html, headers, status_code = fetch_html(args.url)
    if html:
        save_html(html)

        # Step 3: HTML & JS Extraction
        print("[+] Extracting URLs and JS links...")
        result = extract_links_and_scripts(html, args.url)

        print("\n[+] Extracted Endpoints:")
        for url in result["href_links"]:
            print(f"   - {url}")

        with open("results/extracted_links.txt", "w") as f:
            for url in result["href_links"]:
                f.write(url + "\n")

        # Step 4: robots.txt & sitemap.xml
        print("\n[+] Scanning robots.txt and sitemap.xml ...")
        robot_paths = scan_robots_txt(args.url)
        sitemap_urls = scan_sitemap(args.url)

        all_discovered = result["href_links"] + robot_paths + sitemap_urls
        all_discovered = list(set(all_discovered))  # Remove duplicates

        with open("results/all_discovered_links.txt", "w") as f:
            for link in all_discovered:
                f.write(link + "\n")

        print(f"[+] Total endpoints discovered: {len(all_discovered)}")
        print("[+] Saved to results/all_discovered_links.txt")

        # Step 5: Risk Scoring
        print("\n[+] Scoring endpoints based on risk...")
        scored_list = []
        for url in all_discovered:
            score, reason = score_url_reason(url)
            print(f"   - {url} --> [{score} Risk] Reason: {reason}")
            scored_list.append({"url": url, "risk": score, "reason": reason})

        with open("results/scored_endpoints.txt", "w") as f:
            for item in scored_list:
                f.write(f"{item['url']} [{item['risk']}] - {item['reason']}\n")

        # Step 6: Metadata & Report Generation
        metadata = {
            "HTTP Status": status_code,
            "Server": headers.get("Server", "N/A"),
            "Content-Type": headers.get("Content-Type", "N/A"),
            "Tool Version": "ShadowLink v1.0"
        }

        generate_report_files(scored_list, args.url)


if __name__ == "__main__":
    main()
