#!/usr/bin/env python3
"""
TechGuideHQ Toolkit - Master Command Center
Unified Interface for Security Recon, Header Analysis, and Automation
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import os
import socket
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
====================================================================
               TECHGUIDEHQ MASTER TOOLKIT & SECURITY LAB            
        Full-Stack Recon, Automation & Vulnerability Assessment     
===================================================================={Colors.RESET}""")

def run_security_audit():
    target = input(f"\n{Colors.BOLD}[?] Enter target domain or URL (e.g., example.com): {Colors.RESET}").strip()
    if not target:
        target = "example.com"
    
    if not target.startswith('http://') and not target.startswith('https://'):
        url = 'https://' + target
        domain = target
    else:
        url = target
        domain = urlparse(target).netloc

    print(f"\n{Colors.BOLD}[*] Target Acquired: {domain}{Colors.RESET}")
    
    # 1. DNS / IP Resolution
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {Colors.GREEN}[+] Resolved IP Address:{Colors.RESET} {ip}")
    except socket.gaierror as e:
        print(f"  {Colors.FAIL}[!] DNS Resolution Failed:{Colors.RESET} {e}")

    # 2. SSL/TLS Certificate Check
    print(f"  {Colors.CYAN}[*] Inspecting SSL/TLS Certificate...{Colors.RESET}")
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert.get('issuer', []))
                print(f"    {Colors.GREEN}[✓] Issuer:{Colors.RESET} {issuer.get('organizationName', 'Unknown')}")
                print(f"    {Colors.GREEN}[✓] Valid Until:{Colors.RESET} {cert.get('notAfter')}")
    except Exception as e:
        print(f"    {Colors.WARNING}[!] SSL Check Warning:{Colors.RESET} {e}")

    # 3. Security Headers Audit
    print(f"  {Colors.CYAN}[*] Auditing HTTP Security Headers...{Colors.RESET}")
    req = urllib.request.Request(url, headers={'User-Agent': 'TechGuideHQ-SecurityScanner/2.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            headers = dict(resp.headers)
            sec_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']
            for h in sec_headers:
                if headers.get(h) or headers.get(h.lower()):
                    print(f"    {Colors.GREEN}[✓] {h}: Protected{Colors.RESET}")
                else:
                    print(f"    {Colors.WARNING}[!] {h}: Missing (Vulnerability/Risk){Colors.RESET}")
    except Exception as e:
        print(f"    {Colors.FAIL}[!] Header Audit Error:{Colors.RESET} {e}")

def run_watermark_tool():
    print(f"\n{Colors.BOLD}[*] Launching Media Watermarking Utility...{Colors.RESET}")
    watermark_script = "automation/watermark_images.py"
    if os.path.exists(watermark_script):
        os.system(f"python3 {watermark_script}")
    else:
        print(f"  {Colors.FAIL}[!] Error: {watermark_script} not found in repository.{Colors.RESET}")

def main():
    while True:
        print_banner()
        print(f"{Colors.BOLD}Select an Operational Module:{Colors.RESET}")
        print("  [1] Run Web Security Audit & Header Recon")
        print("  [2] Run Media Watermarking Automation")
        print("  [3] Exit Toolkit")
        
        choice = input(f"\n{Colors.CYAN}TechGuideHQ-Toolkit > {Colors.RESET}").strip()
        
        if choice == '1':
            run_security_audit()
        elif choice == '2':
            run_watermark_tool()
        elif choice == '3':
            print(f"\n{Colors.GREEN}[*] Shutting down TechGuideHQ Toolkit. Stay secure.{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid selection. Please choose 1, 2, or 3.{Colors.RESET}")
        
        input(f"\n{Colors.BOLD}[Press Enter to return to main menu]{Colors.RESET}")

if __name__ == "__main__":
    main()
