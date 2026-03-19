import logging
import os
import csv
from datetime import datetime
import json
import time
from curl_cffi import requests, CurlError
from dotenv import load_dotenv
from pathlib import Path

from utils.constants import STOCK_DAILY, STOCK_5MIN, STOCK_30MIN
from utils.util import get_config

load_dotenv()
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")
TWELVE_API_BASE = os.getenv("TWELVE_API_BASE")
START_DATE="2020-01-01 00:00:00"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            browser = "chrome120" if attempt % 2 == 0 else "safari15_3"
            response = requests.get(url, impersonate=browser, timeout=10)
            return response
        except CurlError as e:
            if "TLS connect error" in str(e) or "(35)" in str(e):
                logging.error(f"TLS connect error (try {attempt + 1}/{max_retries})...")
                time.sleep(2)
            else:
                raise e
        except Exception as e:
            logging.error(f"Unknown Error: {e}")
            break

    return None

def fetch_stock_data_freq(symbol, exchange, start_date = "2020-01-01 00:00:00", freq="30min"):
    current_end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_data = []
    seen_dates = set()  # reduce duplication stock price
    logging.info(f"fetch {symbol} ({exchange}) {freq} data...")
    while True:
        url = (
            f"{TWELVE_API_BASE}/time_series?"
            f"symbol={symbol}&interval={freq}&"
            f"apikey={TWELVE_API_KEY}&start_date={start_date}&end_date={current_end_date}&outputsize=5000"
        )
        try:
            response = fetch_with_retry(url)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"Network Error: {e}")
            break
        if data.get("status") != "ok":
            if data.get("code") == 429:
                logging.info("Too Many Requests, Wait 60 seconds...")
                time.sleep(60)
                continue
            else:
                logging.error(f"API Exception: {data.get('message', data)}")
                break
        values = data.get("values", [])
        if not values:
            break
        for item in values:
            date_str = item["datetime"]
            if date_str in seen_dates:
                continue
            seen_dates.add(date_str)
            all_data.append({
                # "symbol": symbol,
                "date": date_str,
                "open": float(item["open"]),
                "high": float(item["high"]),
                "low": float(item["low"]),
                "close": float(item["close"]),
                "volume": int(item["volume"])
            })
        oldest_datetime_in_batch = values[-1]["datetime"]
        if oldest_datetime_in_batch == current_end_date or oldest_datetime_in_batch <= start_date:
            break
        current_end_date = oldest_datetime_in_batch
        time.sleep(8)
    # sort data by timestamp (old data first)
    all_data.sort(key=lambda x: x["date"])
    if all_data:
        os.makedirs(symbol, exist_ok=True)
        file_path = os.path.join(symbol, f"{freq}.csv")
        fieldnames = ["date", "open", "high", "low", "close", "volume"]
        with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()  # 写入表头
            writer.writerows(all_data)  # 批量写入数据
        logging.info(f"Successfully saved {len(all_data)} rows to {file_path}")
    else:
        logging.warning(f"No data fetched for {symbol}.")

def init_fetch_stock_high_freq_data():
    config_data = get_config()
    if config_data:
        stocks = config_data.get("stocks", [])
        freqs = [STOCK_30MIN, STOCK_5MIN, STOCK_DAILY]
        # freqs = ["1min", "5min", "15min", "30min", "45min", "1h", "2h", "4h", "5h", "1day", "1week", "1month"]
        for stock in stocks:
            logging.info(f"fetching TWELVE data: {stock}")
            for freq in freqs:
                fetch_stock_data_freq(stock, "US", START_DATE, freq)
if __name__ == "__main__":
    init_fetch_stock_high_freq_data()