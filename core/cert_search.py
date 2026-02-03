import requests
from utils.ip_tools import is_valid_ip, get_ip

def search_crtsh(domain):
    """
    Query crt.sh to find subdomains and associated IPs.
    Returns a set of unique IPs and a set of subdomains.
    """
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    pass_ips = set()
    pass_domains = set()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                # Extract domain name
                name_value = entry.get('name_value', '')
                subdomains = name_value.split('\n')
                for sub in subdomains:
                    sub = sub.strip()
                    if '*' not in sub and domain in sub:
                         pass_domains.add(sub)
    except Exception as e:
        pass

    # Resolve found subdomains to get fresh IPs
    # Note: This might be slow if there are hundreds, need to be careful in the main loop
    # We will just return the domains mostly, and let the scanner resolve them
    return list(pass_domains)
