from proxychecker import ProxyChecker
from proxyscraper import ProxyScraper
from proxystore import ProxyStore

if __name__ == "__main__":
    proxy_checker = proxychecker(max_concurrent_checks=50)
    results = asyncio.run(proxy_checker.collect_proxies())

    with open('./jsons/working_proxies.jsonc', 'w') as f:
        json.dump(results, f, indent=4)