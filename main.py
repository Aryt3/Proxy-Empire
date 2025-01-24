from proxychecker import ProxyChecker
from proxyscraper import ProxyScraper
from proxystore import ProxyStore
import asyncio, json

if __name__ == "__main__":
    proxy_checker = ProxyChecker(max_concurrent_checks=50)
    results = asyncio.run(proxy_checker.collect_proxies())
