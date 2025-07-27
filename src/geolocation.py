import asyncio
import httpx
from typing import Optional, Dict, Any
from src.config import settings


class GeolocationService:
    """Service for IP geolocation using multiple APIs."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    async def get_location(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Get location information for an IP address."""
        # Пропускаем локальные IP
        if self._is_local_ip(ip_address):
            return {
                "country": "Россия",
                "region": "Локальная сеть",
                "city": "Локальная сеть",
                "latitude": None,
                "longitude": None
            }
        
        # Проверяем кэш
        if ip_address in self.cache:
            return self.cache[ip_address]
        
        # Пробуем разные API в порядке приоритета
        apis = [
            self._try_ipapi_co,
            self._try_ipinfo_io,
            self._try_ip_api_com
        ]
        
        for api_func in apis:
            try:
                result = await api_func(ip_address)
                if result:
                    self.cache[ip_address] = result
                    return result
            except Exception as e:
                print(f"Ошибка API {api_func.__name__}: {e}")
                continue
        
        # Если все API не сработали, возвращаем дефолтные данные
        default_result = {
            "country": "Неизвестно",
            "region": "Неизвестно",
            "city": "Неизвестно",
            "latitude": None,
            "longitude": None
        }
        self.cache[ip_address] = default_result
        return default_result
    
    def _is_local_ip(self, ip: str) -> bool:
        """Check if IP is local."""
        local_prefixes = [
            '127.', '192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.',
            '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
            '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.'
        ]
        return any(ip.startswith(prefix) for prefix in local_prefixes)
    
    async def _try_ipapi_co(self, ip: str) -> Optional[Dict[str, Any]]:
        """Try ipapi.co API."""
        try:
            url = f"http://ip-api.com/json/{ip}"
            response = await self.client.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "country": data.get("country", "Неизвестно"),
                        "region": data.get("regionName", "Неизвестно"),
                        "city": data.get("city", "Неизвестно"),
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon")
                    }
        except Exception as e:
            print(f"Ошибка ipapi.co: {e}")
        return None
    
    async def _try_ipinfo_io(self, ip: str) -> Optional[Dict[str, Any]]:
        """Try ipinfo.io API."""
        try:
            url = f"https://ipinfo.io/{ip}/json"
            response = await self.client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "country": data.get("country", "Неизвестно"),
                    "region": data.get("region", "Неизвестно"),
                    "city": data.get("city", "Неизвестно"),
                    "latitude": data.get("loc", "").split(",")[0] if data.get("loc") else None,
                    "longitude": data.get("loc", "").split(",")[1] if data.get("loc") else None
                }
        except Exception as e:
            print(f"Ошибка ipinfo.io: {e}")
        return None
    
    async def _try_ip_api_com(self, ip: str) -> Optional[Dict[str, Any]]:
        """Try ip-api.com API."""
        try:
            url = f"http://ip-api.com/json/{ip}"
            response = await self.client.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "country": data.get("country", "Неизвестно"),
                        "region": data.get("regionName", "Неизвестно"),
                        "city": data.get("city", "Неизвестно"),
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon")
                    }
        except Exception as e:
            print(f"Ошибка ip-api.com: {e}")
        return None
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Глобальный экземпляр сервиса
geolocation_service = GeolocationService() 