import dns.resolver
from utils.displaying import print_error, print_info

def get_spf_ips(domain):
    """
    Query TXT records to find SPF configurations and extract IPs.
    Returns: list of IPs strings (ipv4).
    """
    found_ips = set()
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            # rdata is usually quoted, e.g. "v=spf1 ..."
            txt_string = rdata.to_text().strip('"')
            if "v=spf1" in txt_string:
                # Parse SPF record
                parts = txt_string.split()
                for part in parts:
                    if part.startswith("ip4:"):
                        ip = part.split("ip4:")[1]
                        found_ips.add(ip)
                    # ip6 support could be added here, but staying with v4 for now
    except Exception as e:
        # print_error(f"SPF Search failed: {e}")
        pass
        
    return list(found_ips)
