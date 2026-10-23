#!/usr/bin/env python3
"""
TechGuideHQ Elite Recursive Web Crawler & Asset Hunter (Stealth Edition)
Performs deep multi-page crawling with browser spoofing and timeout protection.
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse, urljoin
import re
import json
from html.parser import HTMLParser

class BeastParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.in_title = False
        self.links = set()
        self.forms = []
        self.current_form = None
        self.comments = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self.in_title = True
        elif tag == 'a' and 'href' in attrs_dict:
            full_url = urljoin(self.base_url, attrs_dict['href'])
            if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                self.links.add(full_url)
        elif tag == 'form':
            self.current_form = {'action': attrs_dict.get('action', ''), 'method': attrs_dict.get('method', 'get').upper(), 'inputs': []}
            self.forms.append(self.current_form)
        elif tag == 'input' and self.current_form is not None:
            self.current_form['inputs'].append({
                'name': attrs_dict.get('name', ''),
                'type': attrs_dict.get('type', 'text'),
                'value': attrs_dict.get('value', '')
            })

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'form':
            self.current_form = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()

    def handle_comment(self, data):
        cleaned = data.strip()
        if cleaned:
            self.comments.append(cleaned)

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def beast_crawl(start_url, max_pages=5):
    if not start_url.startswith('http://') and not start_url.startswith('https://'):
        start_url = 'https://' + start_url

    visited = set()
    queue = [start_url]
    master_report = {'target': start_url, 'pages_scanned': []}

    print(f"\n{Colors.BOLD}[*] Initializing Stealth Beast Crawler on: {start_url}{Colors.RESET}")

    # Professional browser spoofing header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        
        visited.add(url)
        print(f"  {Colors.CYAN}[+] Crawling ({len(visited)}/{max_pages}): {url}{Colors.RESET}")

        try:
            req = urllib.request.Request(url, headers=headers)
            # Increased timeout to 12s to handle high latency / WAF filtering
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                
                parser = BeastParser(url)
                parser.feed(html)

                emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)))
                phones = list(set(re.findall(r'\+?[0-9][0-9()\-\s]{7,}[0-9]', html)))
                secrets = list(set(re.findall(r'(?:api[_-]?key|secret|token|auth)[=:]["\']([a-zA-Z0-9_\-]{16,})["\']', html, re.IGNORECASE)))

                page_data = {
                    'url': url,
                    'title': parser.title,
                    'forms': parser.forms,
                    'comments': parser.comments,
                    'extracted_emails': emails,
                    'extracted_phones': phones,
                    'potential_secrets': secrets
                }
                master_report['pages_scanned'].append(page_data)

                for link in parser.links:
                    if link not in visited:
                        queue.append(link)

        except Exception as e:
            print(f"    {Colors.WARNING}[!] Connection Handshake Warning / Blocked on {url}: {e}{Colors.RESET}")

    print(f"\n{Colors.GREEN}[✓] Crawl Complete. Saving structured report...{Colors.RESET}")
    report_filename = "beast_scan_report.json"
    with open(report_filename, 'w') as f:
        json.dump(master_report, f, indent=4)
    print(f"  {Colors.BOLD}[+] Report saved to: {report_filename}{Colors.RESET}")

    total_forms = sum(len(p['forms']) for p in master_report['pages_scanned'])
    total_comments = sum(len(p['comments']) for p in master_report['pages_scanned'])
    print(f"  {Colors.GREEN}[✓] Total Pages Scanned:{Colors.RESET} {len(master_report['pages_scanned'])}")
    print(f"  {Colors.GREEN}[✓] Total Forms Mapped:{Colors.RESET} {total_forms}")
    print(f"  {Colors.GREEN}[✓] Total HTML Comments Found:{Colors.RESET} {total_comments}")

def main():
    if len(sys.argv) < 2:
        target = input(f"{Colors.BOLD}[?] Enter target domain to beast crawl: {Colors.RESET}").strip()
        if not target:
            target = "https://example.com"
    else:
        target = sys.argv[1]

    beast_crawl(target)

if __name__ == "__main__":
    main()
