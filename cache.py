import shelve
import time
import os

_CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
_CACHE_PATH = os.path.join(_CACHE_DIR, ".cache_store")
_EXPIRY = 7 * 24 * 3600  # 1 week

def get(ticker):
    with shelve.open(_CACHE_PATH) as db:
        entry = db.get(ticker.upper())
    if not entry:
        return None
    if time.time() - entry["timestamp"] > _EXPIRY:
        return None
    return entry["eps"], entry["pe_ratio"], entry["financial_data"]

def set(ticker, eps, pe_ratio, financial_data):
    with shelve.open(_CACHE_PATH) as db:
        db[ticker.upper()] = {
            "timestamp": time.time(),
            "eps": eps,
            "pe_ratio": pe_ratio,
            "financial_data": financial_data,
        }
