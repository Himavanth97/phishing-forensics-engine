import re
from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    """Normalizes the URL by ensuring it has a protocol scheme."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def is_safe_to_scan(url: str) -> bool:
    """
    Checks if a URL is safe to scan.
    Prevents scanning localhost, private networks, or system protocols to avoid SSRF.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False
            
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Block localhost and local IP ranges
        local_patterns = [
            r'^localhost$',
            r'^127\.\d+\.\d+\.\d+$',
            r'^10\.\d+\.\d+\.\d+$',
            r'^172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+$',
            r'^192\.168\.\d+\.\d+$',
            r'^169\.254\.\d+\.\d+$',
            r'^fc00::',
            r'^fe80::',
            r'^::1$'
        ]
        
        for pattern in local_patterns:
            if re.match(pattern, hostname, re.IGNORECASE):
                return False
                
        return True
    except Exception:
        return False
