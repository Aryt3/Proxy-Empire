from scrapers.main import ProxyScraper
import asyncio, json
from pathlib import Path
from validators.validators import Validator

parent_directory = Path(__file__).parent

PUBLIC_IP, validators = asyncio.run(Validator().sort_validators())

if __name__ == '__main__':
    pass