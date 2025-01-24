from validators.main import ProxyChecker
from scrapers.main import ProxyScraper
from stores.main import ProxyStore
import asyncio
from pathlib import Path

parent_directory = Path(__file__).parent

if __name__ == '__main__':
    proxy_checker = ProxyChecker(max_concurrent_checks=50)
    results = asyncio.run(proxy_checker.collect_proxies())
