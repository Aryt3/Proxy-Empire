import json, aiohttp, asyncio
from aiohttp_socks import ProxyConnector
from aiohttp import ClientTimeout
from utils import handle_exceptions

class ProxyValidator:
    def __init__(self, max_concurrent_checks: int = 50):
        self.timeout_secs = 5
        self.timeout = ClientTimeout(total=self.timeout_secs)
        self.semaphore = asyncio.Semaphore(max_concurrent_checks)


    async def check_proxy(self, proxy_server):
        '''
        Check if a proxy server works for HTTP, SOCKS4, or SOCKS5 protocols.
        '''

        return 
    

    @handle_exceptions
    async def run_validators(self):
        '''
        Function to start application workflow of validating proxies
        '''

        return