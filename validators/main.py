import requests, json, aiohttp, asyncio
from aiohttp_socks import ProxyConnector
from aiohttp import ClientTimeout

class ProxyValidator:
    def __init__(self, max_concurrent_checks: int = 50):
        self.http_proxy_urls = ['https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt', 'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt', 'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt']
        self.timeout_secs = 5
        self.timeout = ClientTimeout(total=self.timeout_secs)
        self.working_proxies = {'http': [], 'socks4': [], 'socks5': []}
        self.semaphore = asyncio.Semaphore(max_concurrent_checks)

    async def check_proxy(self, proxy_server):
        '''
        Check if a proxy server works for HTTP, SOCKS4, or SOCKS5 protocols.
        '''
        async with self.semaphore:
            # Check HTTP
            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    async with session.get('https://httpbin.org/ip', proxy=f'http://{proxy_server}') as response:
                        res = await response.json()
                        if res.get('origin') == proxy_server.split(':')[0]:
                            print(f'Working HTTP proxy: {proxy_server}')
                            self.working_proxies['http'].append(proxy_server)
            except Exception:
                pass

            # Check SOCKS4
            try:
                connector = ProxyConnector.from_url(f'socks4://{proxy_server}')
                async with aiohttp.ClientSession(connector=connector, timeout=self.timeout) as session:
                    async with session.get('https://httpbin.org/ip') as response:
                        res = await response.json()
                        if res.get('origin') == proxy_server.split(':')[0]:
                            print(f'Working SOCKS4 proxy: {proxy_server}')
                            self.working_proxies['socks4'].append(proxy_server)
            except Exception:
                pass

            # Check SOCKS5
            try:
                connector = ProxyConnector.from_url(f'socks5://{proxy_server}')
                async with aiohttp.ClientSession(connector=connector, timeout=self.timeout) as session:
                    async with session.get('https://httpbin.org/ip') as response:
                        res = await response.json()
                        if res.get('origin') == proxy_server.split(':')[0]:
                            print(f'Working SOCKS5 proxy: {proxy_server}')
                            self.working_proxies['socks5'].append(proxy_server)
            except Exception:
                pass

