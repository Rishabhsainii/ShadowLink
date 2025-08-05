# robot_parser.py
import requests
import re
from urllib.parse import urljoin

def scan_robots_txt(base_url):
    robots_url = urljoin(base_url, "/robots.txt")
    print(f"[+] Checking robots.txt: {robots_url}")
    
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            content = response.text
            paths = re.findall(r"(Disallow|Allow):\s*(\/[^\s#]*)", content)
            return [p[1] for p in paths]
        else:
            print("[-] No robots.txt found.")
            return []
    except:
        print("[!] Error accessing robots.txt")
        return []

def scan_sitemap(base_url):
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    print(f"[+] Checking sitemap.xml: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, timeout=5)
        if response.status_code == 200:
            urls = re.findall(r"<loc>(.*?)<\/loc>", response.text)
            return urls
        else:
            print("[-] No sitemap.xml found.")
            return []
    except:
        print("[!] Error accessing sitemap.xml")
        return []
