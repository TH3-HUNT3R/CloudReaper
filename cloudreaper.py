#!/usr/bin/env python3
"""
CloudReaper: The Ultimate Cloudflare Bypass Tool
Author: HUNT3R
"""

import argparse
import sys
import json
import threading
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.layout import Layout
from rich.live import Live

from utils.displaying import console, print_banner, print_info, print_success, print_warning, print_error
from utils.ip_tools import get_ip, is_valid_ip, get_ports_from_args, is_valid_domain
from core.dns_history import search_viewdns
from core.cert_search import search_crtsh
from core.dns_records import get_spf_ips
from core.scanner import scan_subdomains_fast, scan_ports
from core.verifier import verify_bypass, get_page_signature
from utils.waf_detector import is_cloudflare_ip

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="CloudReaper: Cloudflare Bypass")
    parser.add_argument("target", help="Target domain (e.g., example.com)")
    parser.add_argument("--ports", help="Ports to scan", default="80,443,81,8080,8443,8000,8880")
    parser.add_argument("--threads", help="Threads for subdomain scan", type=int, default=20)
    parser.add_argument("--wordlist", help="Path to custom subdomain wordlist", default=None)
    parser.add_argument("--output", help="Save results to JSON file", default=None)
    parser.add_argument("--keyword", help="String that must appear in body to confirm bypass", default=None)
    args = parser.parse_args()

    domain = args.target
    if domain.startswith("http"):
        domain = domain.split("//")[1].split("/")[0]
        if ":" in domain:
            domain = domain.split(":")[0]

    # Validate domain format
    if not is_valid_domain(domain):
        print_error(f"Invalid domain format: '{domain}'")
        console.print("\n[yellow]Expected format:[/yellow] example.com or subdomain.example.com")
        console.print("[yellow]Examples:[/yellow]")
        console.print("  • python cloudreaper.py example.com")
        console.print("  • python cloudreaper.py www.example.com")
        console.print("  • python cloudreaper.py https://example.com\n")
        sys.exit(1)

    target_ports = get_ports_from_args(args.ports)
    target_url = f"https://{domain}" # Baseline assumption

    print_info(f"Starting reconnaissance on: [bold yellow]{domain}[/bold yellow]")
    
    # -1. Pre-Scan: Check if behind Cloudflare
    try:
        target_ip = get_ip(domain)
        if target_ip:
            if not is_cloudflare_ip(target_ip):
                print_success(f"INSTANT WIN! Target {domain} [{target_ip}] is NOT behind Cloudflare.")
                print_info("The target is exposed directly. No bypass needed.")
                
                # Fetch baseline to show it's accessible
                print_info("Fetching baseline signature...")
                baseline = get_page_signature(f"https://{domain}")
                if not baseline:
                    baseline = get_page_signature(f"http://{domain}")
                
                if baseline:
                    print_info(f"Baseline: {baseline['title']} (Size: {baseline['len']}) Server: {baseline['server']}")
                
                # Exit early - no need to scan
                console.print(Panel(
                    f"[bold green]+ REAL IP FOUND: {target_ip}[/bold green]\n\n"
                    f"Target is directly exposed and not using Cloudflare proxy.\n"
                    f"No bypass techniques needed!",
                    title="[bold green]EXPOSED[/bold green]",
                    border_style="green"
                ))
                sys.exit(0)
            else:
                print_warning(f"Target is behind Cloudflare ({target_ip}). Starting bypass...")
    except Exception:
        pass
        
    # 0. Baseline Fingerprint
    print_info("Fetching baseline signature...")
    baseline = get_page_signature(target_url)
    if not baseline:
         # Try HTTP
         target_url = f"http://{domain}"
         baseline = get_page_signature(target_url)
    
    if baseline:
        print_info(f"Baseline: {baseline['title']} (Size: {baseline['len']}) Server: {baseline['server']}")
    else:
        print_warning("Could not fetch baseline. Blind mode engaged.")

    candidates = set()
    
    # Live Dashboard
    with Progress(
        SpinnerColumn(spinner_name="simpleDots", style="bold blue"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        transient=True # Clear on finish to avoid clutter
    ) as progress:
        
        # 1. OSINT: DNS History
        task_dns = progress.add_task("[cyan]Searching DNS History (ViewDNS)...", total=1)
        history_ips = search_viewdns(domain)
        for ip in history_ips:
            candidates.add(("DNS History", ip))
        progress.update(task_dns, advance=1, description=f"[green]DNS History Found: {len(history_ips)} IPs")

        # 2. OSINT: SSL Certificates
        task_crt = progress.add_task("[cyan]Searching Crt.sh Certificates...", total=1)
        cert_domains = search_crtsh(domain)
        # We need to resolve these domains to get IPs
        progress.update(task_crt, description=f"[cyan]Resolving {len(cert_domains)} cert subdomains...")
        
        for sub in cert_domains:
             # Just quick resolve, no fancy thread here for simplicity in this block or could move to scanner
             ip = get_ip(sub)
             if ip:
                 candidates.add(("Cert Search", ip))
        progress.update(task_crt, advance=1, description=f"[green]Cert Search Found subdomains")

        # 3. OSINT: SPF Records (TXT)
        task_spf = progress.add_task("[cyan]Scanning SPF Records...", total=1)
        spf_ips = get_spf_ips(domain)
        for ip in spf_ips:
            candidates.add(("SPF Record", ip))
        progress.update(task_spf, advance=1, description=f"[green]SPF Record Found: {len(spf_ips)} IPs")

        # 4. Subdomain Enumeration
        custom_subs = None
        if args.wordlist:
            try:
                with open(args.wordlist, 'r') as f:
                    custom_subs = [line.strip() for line in f if line.strip()]
                print_info(f"Loaded {len(custom_subs)} subdomains from wordlist.")
            except Exception as e:
                print_error(f"Could not load wordlist: {e}")
        
        task_sub = progress.add_task("[cyan]Brute-forcing Subdomains...", total=100) # Fake total for aesthetics or calc real len
        found_subs = scan_subdomains_fast(domain, threads=args.threads, subdomains=custom_subs)
        for sub, ip in found_subs.items():
            candidates.add(("Subdomain Scan", ip))
        progress.update(task_sub, completed=100, description=f"[green]Subdomains Found: {len(found_subs)}")

    # 4. Filter Unique IPs and Scan Ports
    unique_ips = {ip for source, ip in candidates}
    
    if not unique_ips:
        print_error("No candidate IPs found.")
        sys.exit(1)

    print_info(f"Scanning {len(unique_ips)} unique candidate IPs for exposed ports...")
    
    results_table = Table(title="Bypass Candidates", border_style="bold green")
    results_table.add_column("Source IP", style="cyan")
    results_table.add_column("Port", style="magenta")
    results_table.add_column("Server Header", style="dim")
    results_table.add_column("Match Score", style="bold yellow")
    results_table.add_column("Bypass?", style="bold red")

    found_bypass = False
    json_results = []
    
    for ip in unique_ips:
        open_ports = scan_ports(ip, target_ports)
        if not open_ports:
            continue
            
        for port in open_ports:
            score, sig = verify_bypass(target_url, ip, port, keyword=args.keyword)
            
            bypass_str = "[dim]No[/dim]"
            if score > 70:
                bypass_str = "[bold green]YES![/bold green]"
                found_bypass = True
            elif score > 40:
                bypass_str = "[chartreuse3]Likely[/chartreuse3]" # Neon look
            
            if sig:
                results_table.add_row(
                    ip, 
                    str(port), 
                    sig.get('server', 'unknown')[:20], 
                    f"{score}%", 
                    bypass_str
                )
                
                if args.output:
                    json_results.append({
                        "ip": ip,
                        "port": port,
                        "server": sig.get('server', 'unknown'),
                        "score": score,
                        "bypass_likely": score > 40,
                        "confirmed": score > 70
                    })

    console.print(results_table)

    if found_bypass:
        print_success("Bypass Discovered! The origin server is exposed.")
    else:
        print_warning("No direct bypass confirmed, but check the 'Likely' candidates manually.")

    if args.output and json_results:
        try:
            with open(args.output, 'w') as f:
                json.dump(json_results, f, indent=4)
            print_success(f"Results saved to {args.output}")
        except Exception as e:
            print_error(f"Failed to save JSON: {e}")

if __name__ == "__main__":
    main()
