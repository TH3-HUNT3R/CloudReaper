import socket
import ipaddress
import re

def get_ip(domain):
    """Resolve domain to IP."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def is_valid_ip(ip):
    """Check if string is a valid IP."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_domain(domain):
    """
    Check if string is a valid domain format.
    Returns True if domain matches valid domain pattern.
    """
    # Domain regex pattern
    # - Must have at least one dot
    # - Can contain alphanumeric, hyphens, and dots
    # - TLD must be at least 2 characters
    # - Cannot start or end with hyphen or dot
    # - Each label (part between dots) must be 1-63 characters
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    
    if not domain or len(domain) > 253:
        return False
    
    return bool(domain_pattern.match(domain))

def get_ports_from_args(port_str):
    """Parse port string "80,443" into list of ints."""
    try:
        return [int(p.strip()) for p in port_str.split(',')]
    except ValueError:
        # Extended Cloudflare Bypass List
        return [
            80, 443, 8080, 8443, 
            2052, 2053, 2082, 2083, 2086, 2087, 2095, 2096, 
            8880, 81, 3000
        ]
