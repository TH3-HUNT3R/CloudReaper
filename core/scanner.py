import socket
import requests
import concurrent.futures
from utils.displaying import console
from utils.ip_tools import is_valid_ip, get_ip

DNS_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk", "ns2", 
    "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test", "ns", "blog", 
    "pop3", "dev", "www2", "admin", "forum", "news", "email", "ns3", "mail2", "ne1", 
    "apps", "beta", "shop", "api", "support", "secure", "direct", "origin", "backend",
    "portal", "remote", "vpn", "staging", "development"
]

def check_port(ip, port, timeout=1.5):
    """Check if a port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def check_subdomain(domain, sub):
    """Resolve a subdomain."""
    target = f"{sub}.{domain}"
    ip = get_ip(target)
    if ip:
        return (target, ip)
    return None

def scan_ports(ip, ports):
    """Scan a list of ports on an IP."""
    open_ports = []
    for port in ports:
        if check_port(ip, port):
            open_ports.append(port)
    return open_ports

def scan_subdomains_fast(domain, threads=20, subdomains=None):
    """Threaded subdomain scanner."""
    if subdomains is None:
        subdomains = DNS_SUBDOMAINS
    found = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_sub = {executor.submit(check_subdomain, domain, sub): sub for sub in subdomains}
        for future in concurrent.futures.as_completed(future_to_sub):
            result = future.result()
            if result:
                subdomain, ip = result
                found[subdomain] = ip
    return found
