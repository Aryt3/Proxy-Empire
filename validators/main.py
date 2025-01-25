import asyncio
from aiohttp_socks import ProxyConnector
from aiohttp import ClientTimeout
from utils import handle_exceptions

class ProxyValidator:
    def __init__(self, max_concurrent_checks: int = 1000):
        self.timeout_secs = 2
        self.timeout = ClientTimeout(total=self.timeout_secs)
        self.semaphore = asyncio.Semaphore(max_concurrent_checks)
    

    @handle_exceptions
    async def run_validators(self):
        '''
        Function to start application workflow of validating proxies
        '''

        return
    

    @handle_exceptions
    async def portscan(self, target, port):
        '''
        Check if a proxy at a specific port is accessible.
        '''

        # Create a TCP connection to the target on the specified port
        reader, writer = await asyncio.open_connection(target, port)
        writer.close() 
        await writer.wait_closed() 
        return True


    @handle_exceptions
    async def scan_single_port(self, proxy):
        '''
        Scan a single proxy (host and port).
        '''
        
        async with self.semaphore:
            # Check the proxy's port status and return it if it's up
            is_up = await self.portscan(proxy['host'], proxy['port'])
            return proxy if is_up else None


    @handle_exceptions
    async def validate_proxies(self, proxies):
        '''
        Validate a list of proxies and return only the ones that are online.
        '''

        tasks = [self.scan_single_port(proxy) for proxy in proxies]
        
        # Gather results and filter out the None values (proxies that are down)
        results = await asyncio.gather(*tasks)
        online_proxies = [proxy for proxy in results if proxy is not None]
        
        return online_proxies