import os
import json
import logging

from utils.constants import STOCK_DAILY, STOCK_30MIN, STOCK_5MIN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_config():
    current_file_path = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(current_file_path))
    config_path = os.path.join(project_dir, 'config.json')
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        return config_data
    except FileNotFoundError:
        logging.ERROR("Not found config.json")
    except json.JSONDecodeError:
        logging.ERROR("Error format: config.json")

def get_stock_data_csv_path(stock, freq):
    global csv_path
    current_file_path = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(current_file_path))
    if freq == STOCK_DAILY:
        csv_path = os.path.join(project_dir, f'stock_data/{stock}', '1day.csv')
    elif freq == STOCK_30MIN:
        csv_path = os.path.join(project_dir, f'stock_data/{stock}', '30min.csv')
    elif freq == STOCK_5MIN:
        csv_path = os.path.join(project_dir, f'stock_data/{stock}', '5min.csv')
    return csv_path