from scrapers.main import ProxyScraper
import asyncio, json
from pathlib import Path
from validators.validators import Validator

parent_directory = Path(__file__).parent

if __name__ == '__main__':
    asyncio.run(ProxyScraper().run_scrapers())