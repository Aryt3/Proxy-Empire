import aiohttp, asyncio, re
from aiohttp import ClientTimeout
from scrapers import http_proxy_list, socks4_proxy_list, socks5_proxy_list
from utils import handle_exceptions
from stores.main import ProxyStore
from stores.model.schemas import Proxy_Schema
from validators.main import ProxyValidator

class ProxyScraper:
    def __init__(self, max_concurrent_checks: int = 50):
        self.http_proxy_urls = http_proxy_list
        self.socks4_proxy_urls = socks4_proxy_list
        self.socks5_proxy_urls = socks5_proxy_list

        self.timeout_secs = 5
        self.timeout = ClientTimeout(total=self.timeout_secs)
        self.semaphore = asyncio.Semaphore(max_concurrent_checks)

        self.ipv4_regex = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        self.ipv6_regex = r'^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})'
        self.domain_regex = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z0-9-]{2,}\.?'

    def _extract_proxy(self, line: str, url: str, protocol):
        '''
        Helper-Function to return a parsed proxy as dictionary
        '''
        
        # Check for IPv4
        if re.match(self.ipv4_regex, line):
            # IPv4 format: host:port
            res = {
                'host': line.split(':')[0],
                'port': int(line.split(':')[1]),
                'origin': url
            }

        # Check for IPv6
        elif re.match(self.ipv6_regex, line):
            # IPv6 format: [host]:port
            # Note: IPv6 addresses are enclosed in brackets, e.g., [2001:db8::1]:8080
            if ':' in line:
                host_port = line.split(']')  # Split by closing bracket
                host = host_port[0][1:]  # Remove the opening '['
                port = int(host_port[1][1:])  # Remove the ':'
            else:
                host = line
                port = None

            res = {
                'host': host,
                'port': port,
                'origin': url,
            }

        # Check for domain
        elif re.match(self.domain_regex, line):
            # Domain format: host:port
            host_port = line.split(':')
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else None
            
            res = {
                'host': host,
                'port': port,
                'origin': url
            }

        else:
            res = {}

        res['protocol'] = protocol

        return res


    @handle_exceptions
    async def fetch_proxies(self, session, url, protocol):
        '''
        Fetch proxies from a URL asynchronously
        '''
            
        async with session.get(url, timeout=self.timeout) as response:
            text = await response.text()

            # Return stripped proxies from the URL along with the source URL
            return [self._extract_proxy(line.strip(), url, protocol) for line in text.splitlines() if line.strip()]


    @handle_exceptions
    async def collect_txt_files(self):
        '''
        Collect all proxies from URLs and check their usability asynchronously.
        '''
        async with aiohttp.ClientSession() as session:
            # Create tasks for each proxy URL to fetch proxies concurrently
            tasks = []
            tasks.extend([self.fetch_proxies(session, url, 'http') for url in self.http_proxy_urls])
            tasks.extend([self.fetch_proxies(session, url, 'socks4') for url in self.socks4_proxy_urls])
            tasks.extend([self.fetch_proxies(session, url, 'socks5') for url in self.socks5_proxy_urls])

            # Run all tasks in parallel and await their completion
            all_proxies = await asyncio.gather(*tasks)

            # Flatten the list of proxies from all URLs along with their source
            all_proxies = [proxy for sublist in all_proxies for proxy in sublist]

        return all_proxies
    

    @handle_exceptions
    async def run_scrapers(self):
        '''
        Function to start application workflow of gathering proxies
        '''

        proxies = await self.collect_txt_files()

        await ProxyStore().batch_add_proxies([Proxy_Schema(**proxy) for proxy in proxies])

        asyncio.create_task(ProxyValidator().run_validators())

        return