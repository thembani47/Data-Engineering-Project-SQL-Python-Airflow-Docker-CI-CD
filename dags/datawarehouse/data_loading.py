import json
from datetime import date
import logging

logger = logging.getLogger(__name__)

def load_data():
    file_path = f"./data/youtube_data_{date.today()}.json"

    try:
        logger.info(f"Processing data from {file_path}")
        with open(file_path, "r") as raw_data:
            data = json.load(raw_data)

        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {file_path}")
        raise

