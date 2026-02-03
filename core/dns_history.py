import requests
from bs4 import BeautifulSoup
from utils.displaying import console, print_info, print_error
from utils.ip_tools import is_valid_ip

def search_viewdns(domain):
    """
    Search ViewDNS.info for historical IP addresses.
    Parses the HTML table from the 'iphistory' page.
    """
    url = f"https://viewdns.info/iphistory/?domain={domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    found_ips = set()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # The data is usually in a table with id="null" or just a table inside content
            # Strategy: Find table rows <tr> and check for IPs
            table = soup.find('table', border="1")
            
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]: # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        # owner = cols[2].text.strip() # Optional: check owner
                        if is_valid_ip(ip):
                            found_ips.add(ip)
    except Exception as e:
        # print_error(f"ViewDNS Error: {e}")
        pass # Fail silently/gracefully
        
    return list(found_ips)
