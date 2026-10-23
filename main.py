#!/usr/bin/env python3
"""
TechGuideHQ Toolkit - All-in-One Security Recon & Vulnerability Engine
Unified Self-Contained Enterprise Security Suite
Author: TechGuideHQ (@TechGuideHQ1)
License: MIT
"""

import sys
import socket
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
====================================================================
           TECHGUIDEHQ ALL-IN-ONE SECURITY & VULN ENGINE            
    Recon, TLS Inspection, CORS Auditing & PHP Weakness Probing     
===================================================================={Colors.RESET}""")

def run_comprehensive_audit():
    target = input(f"\n{Colors.BOLD}[?] Enter target domain or URL (e.g., example.com): {Colors.RESET}").strip()
    if not target:
        target = "example.com"
    
    if not target.startswith('http://') and not target.startswith('https://'):
        url = 'https://' + target
        domain = target
    else:
        url = target
        domain = urlparse(target).netloc

    print(f"\n{Colors.BOLD}[+] Target Profile Initialized: {domain}{Colors.RESET}")

    # 1. DNS & IP Resolution
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {Colors.GREEN}[✓] Resolved IPv4 Address:{Colors.RESET} {ip}")
    except socket.gaierror as e:
        print(f"  {Colors.FAIL}[!] DNS Resolution Failed:{Colors.RESET} {e}")
        return

    # 2. TLS/SSL & Cipher Suite Inspection
    print(f"  {Colors.CYAN}[*] Inspecting TLS Handshake & Cipher Security...{Colors.RESET}")
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                issuer = dict(x[0] for x in cert.get('issuer', []))
                print(f"    {Colors.GREEN}[✓] Cipher Suite:{Colors.RESET} {cipher[0]} ({cipher[1]} bits)")
                print(f"    {Colors.GREEN}[✓] Certificate Issuer:{Colors.RESET} {issuer.get('organizationName', 'Unknown')}")
                print(f"    {Colors.GREEN}[✓] Expiration Date:{Colors.RESET} {cert.get('notAfter')}")
    except Exception as e:
        print(f"    {Colors.WARNING}[!] TLS Handshake Warning / WAF Blocked: {e}{Colors.RESET}")

    # 3. HTTP Header Security Audit & PHP Exposure Check
    print(f"  {Colors.CYAN}[*] Auditing Security Headers & PHP Stack Exposure...{Colors.RESET}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (TechGuideHQ-AuditEngine/5.0)'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            headers = dict(resp.headers)
            
            # Check Technology Disclosure
            powered_by = headers.get('X-Powered-By') or headers.get('x-powered-by')
            if powered_by:
                print(f"    {Colors.WARNING}[!] Information Disclosure: X-Powered-By -> '{powered_by}'{Colors.RESET}")
                if 'php' in powered_by.lower():
                    print(f"    {Colors.FAIL}[!] PHP Application Stack Identified!{Colors.RESET}")
            else:
                print(f"    {Colors.GREEN}[✓] X-Powered-By header hidden.{Colors.RESET}")

            # Security Headers Checklist
            sec_headers = {
                'Strict-Transport-Security': 'HSTS (Protocol Downgrade Defense)',
                'Content-Security-Policy': 'CSP (XSS & Injection Defense)',
                'X-Frame-Options': 'Clickjacking Defense',
                'X-Content-Type-Options': 'MIME-Sniffing Defense'
            }
            for header, desc in sec_headers.items():
                if headers.get(header) or headers.get(header.lower()):
                    print(f"    {Colors.GREEN}[Secure] {header}{Colors.RESET}")
                else:
                    print(f"    {Colors.WARNING}[Missing Risk] {header} -> {desc}{Colors.RESET}")

    except Exception as e:
        print(f"    {Colors.FAIL}[!] Header Audit Timed Out or Blocked: {e}{Colors.RESET}")

    # 4. CORS Misconfiguration Audit
    print(f"  {Colors.CYAN}[*] Testing CORS Policy Misconfigurations...{Colors.RESET}")
    test_origin = "https://evil-attacker-domain.com"
    cors_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Origin': test_origin})
    try:
        with urllib.request.urlopen(cors_req, timeout=6) as cors_resp:
            acao = cors_resp.headers.get('Access-Control-Allow-Origin')
            if acao == '*':
                print(f"    {Colors.WARNING}[!] Vulnerability: Wildcard CORS ('*') enabled.{Colors.RESET}")
            elif acao == test_origin:
                print(f"    {Colors.FAIL}[!] Critical Flaw: Reflected Origin trusted ({test_origin}).{Colors.RESET}")
            else:
                print(f"    {Colors.GREEN}[✓] CORS Policy Isolated Securely.{Colors.RESET}")
    except Exception:
        print(f"    {Colors.DIM}[i] CORS probe restricted or blocked by target firewall.{Colors.DIM}")

    # 5. Sensitive PHP File & Endpoint Probing
    print(f"  {Colors.CYAN}[*] Probing Sensitive PHP & Config Endpoints...{Colors.RESET}")
    sensitive_paths = ['/phpinfo.php', '/config.php', '/.env', '/wp-login.php']
    for path in sensitive_paths:
        test_url = f"https://{domain}{path}"
        try:
            sub_req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(sub_req, timeout=4) as sub_resp:
                if sub_resp.status == 200:
                    print(f"    {Colors.FAIL}[!] Critical Finding: Exposed Endpoint -> {test_url}{Colors.RESET}")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"    {Colors.GREEN}[Protected] {path} (HTTP 403){Colors.RESET}")
        except Exception:
            pass

def main():
    while True:
        print_banner()
        print(f"{Colors.BOLD}Select an Option:{Colors.RESET}")
        print("  [1] Run All-in-One Security & Vulnerability Audit")
        print("  [2] Exit Toolkit")
        
        choice = input(f"\n{Colors.CYAN}TechGuideHQ-Toolkit > {Colors.RESET}").strip()
        
        if choice == '1':
            run_comprehensive_audit()
        elif choice == '2':
            print(f"\n{Colors.GREEN}[*] Shutting down toolkit. Stay elite.{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid selection.{Colors.RESET}")
        
        input(f"\n{Colors.BOLD}[Press Enter to return to menu]{Colors.RESET}")

if __name__ == "__main__":
    main()
