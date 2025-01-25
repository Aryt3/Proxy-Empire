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

        self.proxy_regex = [
            r"((?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}):([0-9]{1,5})"
        ]


    def _extract_proxies(self, text: str, url: str, protocol: str):
        """
        Extract proxies from text and return them as a list of dictionaries.
        """

        proxies = []

        for pattern in self.proxy_regex:
            matches = re.findall(pattern, text)

            for host, port in matches:
                proxies.extend([{
                    'host': host,
                    'port': port,
                    'protocol': protocol
                }])

        return proxies


    @handle_exceptions
    async def fetch_proxies(self, session, url, protocol):
        '''
        Fetch proxies from a URL asynchronously
        '''
            
        async with session.get(url, timeout=self.timeout) as response:
            text = await response.text()

            # Return stripped proxies from the URL along with the source URL
            return self._extract_proxies(text, url, protocol)


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
            all_proxies = [proxy for sublist in all_proxies if sublist for proxy in sublist if proxy]

            print(all_proxies)

        return all_proxies
    

    @handle_exceptions
    async def run_scrapers(self):
        '''
        Function to start application workflow of gathering proxies
        '''

        proxies = await self.collect_txt_files()

        print(len(proxies))

        # Deduplicate by using a set of tuples
        unique_proxies = list({(proxy['host'], proxy['port'], proxy['protocol']) for proxy in proxies})

        # Convert back to a list of dictionaries
        unique_proxies = [{'host': host, 'port': port, 'protocol': protocol} for host, port, protocol in unique_proxies]

        print(len(unique_proxies))

        await ProxyStore().batch_add_proxies([Proxy_Schema(**proxy) for proxy in unique_proxies])

        asyncio.create_task(ProxyValidator().run_validators())

        return