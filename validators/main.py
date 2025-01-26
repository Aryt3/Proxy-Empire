import asyncio, aiohttp, random, time
from aiohttp import ClientTimeout
from utils import handle_exceptions, silence
from validators.validators import Validator
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

PUBLIC_IP, validators = asyncio.run(Validator().sort_validators())

class ProxyValidator:
    def __init__(self, max_concurrent_checks: int = 1000):
        self.timeout_secs = 10
        self.timeout = ClientTimeout(total=self.timeout_secs)
        self.semaphore = asyncio.Semaphore(max_concurrent_checks)
    

    @silence
    async def check_proxy(self, proxy_host, proxy_port, proxy_protocol):
        '''
        Function to validate if a proxy actually works
        '''

        validator = random.choice(validators)

        proxy_protocol = proxy_protocol if proxy_protocol != 'https' else 'http'

        proxy_url = f'{proxy_protocol}://{proxy_host}:{proxy_port}'

        connector = ProxyConnector.from_url(proxy_url)

        async with aiohttp.ClientSession(connector=connector) as session:
            start_time = time.perf_counter()
            async with session.get(validator.url, timeout=self.timeout) as response:
                elapsed_time = time.monotonic() - start_time

                if validator.type == 'json':
                    res = await response.json()

                    if proxy_host == res.get(validator.json_key):
                        latency = elapsed_time

                else:
                    res = await response.text()

                    if proxy_host == res.strip():
                        latency = elapsed_time
                    
                    
                if latency:
                    return {
                        'host': proxy_host,
                        'port': proxy_port,
                        'protocol': proxy_protocol,
                        'latency': int(latency * 1000)
                    }
                return None

    @silence
    async def portscan(self, target, port):
        '''
        Check if a proxy at a specific port is accessible.
        '''

        # Create a TCP connection to the target on the specified port
        reader, writer = await asyncio.open_connection(target, port)
        writer.close() 
        await writer.wait_closed() 
        return True


    @silence
    async def scan_single_port(self, proxy):
        '''
        Scan a single proxy (host and port).
        '''
        
        async with self.semaphore:
            # Check the proxy's port status and return it if it's up
            is_up = await self.portscan(proxy['host'], proxy['port'])
            
            if is_up:
                # print(f"[?] Proxy active on host {proxy['host']} via port {proxy['port']}")
                res = await self.check_proxy(proxy_host=proxy.get('host'), proxy_port=proxy.get('port'), proxy_protocol=proxy.get('protocol'))

                if res:
                    print(f"[?] Found working Proxy: {res.get('host')}:{res.get('port')}, protocol: {res.get('protocol')}, latency: {res.get('latency')}")
                    return res
                

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