from model.database import DBAsyncSession
from model.models import (
    Proxy,
    Update
)
from model.schemas import (
    Proxy_Schema
)
from model.data_classes import (
    ProtocolEnum,
    CountryEnum
)
from utils import handle_exceptions


class ProxyStore:

    def __init__(self):
        pass

    
    async def get_proxy_list(self, proxy_data):
        return 
    
    
    async def get_proxy(self, proxy_data):
        return 


    @handle_exceptions
    async def add_proxy(self, proxy_data: Proxy_Schema):
        '''
        Function to add new proxies to the database
        '''

        async with DBAsyncSession() as db:
            db.add(Proxy(
                host=proxy_data.host,
                port=proxy_data.port,
                protocol=ProtocolEnum(proxy_data.protocol),
                anonymity=proxy_data.anonymity,
                country=CountryEnum(proxy_data.country),
                latency=proxy_data.latency,
                secret=proxy_data.secret,
                last_ts=proxy_data.last_ts,
                ip_score=proxy_data.ip_score,
                active=proxy_data.active
            ))
            await db.commit()


    async def update_proxy(self, proxy_data):
        return 