# app.py (your main FastAPI app)

import asyncio
from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

alert_cache = {}

# TTL mapping (per alert type)
TTL_CONFIG = {
    "Brute Force Password Attempt": 300,       # 5 min
    "Credential Stuffing Attempt": 300,
    "Suspicious API Usage": 300,
    "Malware / Bot Behaviour": 300,
    "Impossible Travel": 1800,                    # 30 min
    "Account Takeover": 1800,
    "Privilege Escalation Attempt": 1800,
    "Data Exfiltration": 18000,                   # 5 hr
    "Insider Misuse": 18000,
    "Network Anomaly": 18000,
}


async def cache_cleaner():
    """Periodically clean expired alerts from cache."""
    try:
        while True:
            now = datetime.utcnow()
            expired = [k for k, v in alert_cache.items() if v < now]
            for k in expired:
                del alert_cache[k]
            await asyncio.sleep(300)  # every 5 min
    except asyncio.CancelledError:
        print("Cache cleaner stopped")


def is_duplicate(alert_id: str, alert_name: str) -> bool:
    now = datetime.utcnow()
    ttl = TTL_CONFIG.get(alert_name, 600)  # fallback = 10 min
    # If alert_id exists and not expired → duplicate
    if alert_id in alert_cache and alert_cache[alert_id] > now:
        return True

    # Otherwise update cache with new expiry
    alert_cache[alert_id] = now + timedelta(seconds=ttl)
    return False




