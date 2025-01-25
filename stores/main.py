from sqlalchemy.future import select
from sqlalchemy.sql import and_
from stores.model.database import DBAsyncSession
from stores.model.models import (
    Proxy,
    Update,
    Proxy_Origin
)
from stores.model.schemas import (
    Proxy_Schema,
    Proxy_Filter_Schema,
    Update_Schema,
    Proxy_Origin_Schema
)
from stores.model.data_classes import (
    ProtocolEnum,
    CountryEnum
)
from utils import handle_exceptions
from enum import Enum


class ProxyStore:

    def __init__(self):
        pass

    #
    # Helper-Functions
    #
    
    def _serialize_proxy(self, proxy):
        '''
        Helper Function to convert Datbase Tables to python dictionaries
        This Function also extracts values of Enum-Columns
        '''

        return {
            column.name: (
                getattr(proxy, column.name).value
                if isinstance(getattr(proxy, column.name), Enum)
                else getattr(proxy, column.name)
            )
            for column in Proxy.__table__.columns
        }
    
    #
    # Functions to query database
    #
    
    @handle_exceptions
    async def get_proxy_list(self, proxy_filter: Proxy_Filter_Schema):
        '''
        Function to get a list of all stored proxies.
        There are different filtering options to only get a specific portion
        '''

        async with DBAsyncSession() as db:
            query = select(Proxy)
            filters = []

            # Map filters dynamically based on Proxy_Filter_Schema attributes
            for field, value in proxy_filter.dict(exclude_unset=True).items():
                if value is not None:
                    # Special handling for min_latency and max_latency
                    if field == 'min_latency':
                        filters.append(Proxy.latency > value)
                    elif field == 'max_latency':
                        filters.append(Proxy.latency < value)
                    else:
                        # Default handling for other fields
                        filters.append(getattr(Proxy, field) == value)

            # Apply all filters dynamically
            if filters:
                query = query.where(and_(*filters))

            db_res = await db.execute(query)
            proxy_list = db_res.scalars().all()

        return [self._serialize_proxy(proxy) for proxy in proxy_list]
    
    
    @handle_exceptions
    async def get_proxy(self, proxy_id: str):
        '''
        Function to get information on a single proxy 
        '''

        async with DBAsyncSession() as db:
            db_res = await db.execute(select(Proxy).filter(Proxy.id == proxy_id))
            proxy = db_res.scalars().first()

        return self._serialize_proxy(proxy)
    

    @handle_exceptions
    async def get_proxy_updates(self, proxy_id: str):
        '''
        Function to get all updates for a single proxy
        '''

        async with DBAsyncSession() as db:
            db_res = await db.execute(select(Update).filter(Update.pid == proxy_id))
            proxy_list = db_res.scalars().all()

        return [self._serialize_proxy(proxy) for proxy in proxy_list]


    #
    # Functions to add new database entries
    #

    @handle_exceptions
    async def add_proxy(self, proxy: Proxy_Schema):
        '''
        Function to add new proxies to the database
        '''

        async with DBAsyncSession() as db:
            db.add(Proxy(
                host=proxy.host,
                port=proxy.port,
                protocol=ProtocolEnum(proxy.protocol),
                anonymity=proxy.anonymity,
                country=CountryEnum(proxy.country),
                latency=proxy.latency,
                secret=proxy.secret,
                last_ts=proxy.last_ts,
                ip_score=proxy.ip_score,
                active=proxy.active
            ))
            await db.commit()

        return
    

    @handle_exceptions
    async def batch_add_proxies(self, proxies: list[Proxy_Schema]):
        '''
        Function to add a batch of proxies
        '''

        async with DBAsyncSession() as db:
            # Create a list of Proxy objects
            proxy_objects = [
                Proxy(
                    host=proxy.host,
                    port=proxy.port,
                    protocol=ProtocolEnum(proxy.protocol),
                    anonymity=proxy.anonymity,
                    country=CountryEnum(proxy.country),
                    latency=proxy.latency,
                    secret=proxy.secret,
                    last_ts=proxy.last_ts,
                    ip_score=proxy.ip_score,
                    active=proxy.active
                ) for proxy in proxies
            ]
            
            # Add all proxies at once
            db.add_all(proxy_objects)

            await db.commit()
        
        return


    @handle_exceptions
    async def update_proxy(self, proxy_update: Update_Schema):
        '''
        Function to update an exisiting proxy 
        '''

        async with DBAsyncSession() as db:
            db.add(Update(
                pid=proxy_update.pid,
                ts=proxy_update.ts,
                latency=proxy_update.latency
            ))
            await db.commit()

        return
    

    @handle_exceptions
    async def add_origin(self, proxy_origin: Proxy_Origin_Schema):
        '''
        Function to add origin/source of an existing proxy
        '''

        async with DBAsyncSession() as db:
            # Check if Proxy_Origin with same pid and source already exists
            existing_origin = await db.execute(
                select(Proxy_Origin).filter(
                    Proxy_Origin.pid == proxy_origin.pid,
                    Proxy_Origin.source == proxy_origin.source
                )
            )
            existing_origin = existing_origin.scalars().first()

            if existing_origin:
                return 
            
            # add new origin if it doesn't exist
            db.add(Proxy_Origin(
                pid=proxy_origin.pid,
                ts=proxy_origin.ts,
                source=proxy_origin.source
            ))

        return