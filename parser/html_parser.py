# html_parser.py
from bs4 import BeautifulSoup
import re

def extract_links_and_scripts(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    found_urls = set()

    # Extract <a href="...">
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        if href.startswith("http") or href.startswith("/"):
            found_urls.add(href)

    # Extract <script src="...">
    script_links = []
    for tag in soup.find_all("script", src=True):
        src = tag['src']
        if src.startswith("http") or src.startswith("/"):
            script_links.append(src)
            found_urls.add(src)

    # Extract inline JS content
    inline_scripts = soup.find_all("script", src=False)
    inline_urls = []
    for script in inline_scripts:
        if script.string:
            urls = re.findall(r'\/[a-zA-Z0-9_\-\/\.]*', script.string)
            inline_urls.extend(urls)
            found_urls.update(urls)

    return {
        "href_links": list(found_urls),
        "script_links": script_links,
        "inline_urls": inline_urls
    }
