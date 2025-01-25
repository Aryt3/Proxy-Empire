from scrapers.main import ProxyScraper
import asyncio
from pathlib import Path

parent_directory = Path(__file__).parent

if __name__ == '__main__':
    asyncio.run(ProxyScraper().scrape_all())
