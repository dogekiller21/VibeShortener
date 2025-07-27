from fastapi import Request
from typing import Optional


def get_real_ip(request: Request) -> Optional[str]:
    """
    Get real IP address from request, handling proxy headers.
    
    Priority order:
    1. X-Forwarded-For (first IP in chain)
    2. X-Real-IP
    3. X-Client-IP
    4. CF-Connecting-IP (Cloudflare)
    5. request.client.host (fallback)
    """
    # Check X-Forwarded-For header
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs: "client, proxy1, proxy2"
        # We want the first one (original client IP)
        real_ip = forwarded_for.split(",")[0].strip()
        if real_ip and real_ip != "unknown":
            return real_ip
    
    # Check X-Real-IP header
    real_ip = request.headers.get("x-real-ip")
    if real_ip and real_ip != "unknown":
        return real_ip
    
    # Check X-Client-IP header
    client_ip = request.headers.get("x-client-ip")
    if client_ip and client_ip != "unknown":
        return client_ip
    
    # Check Cloudflare header
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip and cf_ip != "unknown":
        return cf_ip
    
    # Fallback to request.client.host
    if request.client:
        return request.client.host
    
    return None 