import requests
import json
import time
import os

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

class CurrencyConverter:
    def __init__(self, cache_expiry: int = 3600, cache_file: str = "exchange_rates.json"):
        self.cache_expiry = cache_expiry
        self.cache_file = cache_file

    @property
    def rates(self) -> dict[str, float]:
        rates = self._load_from_cache()
        if rates is None:
            rates = self._fetch_rates()
            self._save_to_cache(rates)
        return rates

    def _load_from_cache(self) -> dict[str, float] | None:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    if time.time() - data['timestamp'] < self.cache_expiry:
                        return data['rates']
            except (json.JSONDecodeError, KeyError):
                print("Invalid cache file. Fetching from API.")
        return None

    def _save_to_cache(self, rates: dict[str, float]) -> None:
        try:
            data = {'timestamp': time.time(), 'rates': rates}
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Error saving to cache: {e}")

    def _fetch_rates(self) -> dict[str, float]:
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            return data["rates"]
        except Exception as e:
            raise Exception(f"Error fetching exchange rates: {e}")

    def convert(self, amount: float, currency: str) -> float:
        rate = self.rates.get(currency)
        if rate is None:
            raise ValueError(f"Unsupported currency: {currency}")
        return amount * rate

