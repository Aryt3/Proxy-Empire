from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from model.data_classes import (
    ProtocolEnum,
    CountryEnum
)

Base = declarative_base()

class Proxy(Base):
    '''
    Database Table to store the main information about a proxy
    '''

    __tablename__ = 'proxies'

    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()), unique=True) 
    host = Column(String(length=255), nullable=False) 
    port = Column(Integer(), nullable=False) 
    protocol = Column(Enum(ProtocolEnum), nullable=False) 
    anonymity = Column(String(length=255), nullable=True) 
    country = Column(Enum(CountryEnum), nullable=True) 
    latency = Column(Integer(), nullable=True) # Latency in ms
    secret = Column(String(length=255), nullable=True)
    last_ts = Column(Integer(), nullable=True) # Unix-Timestamp
    ip_score = Column(String(length=255), nullable=True)
    active = Column(Boolean(), nullable=False)

    def __repr__(self):
        return f'Proxy(id={self.id}, host={self.host}, port={self.port}, protocol={self.protocol}, anonymity={self.anonymity}, country={self.country}, latency={self.latency}, secret={self.secret}, last_ts={self.last_ts}, ip_score={self.ip_score}, active={self.active})'


class Update(Base):
    '''
    Database Table to store every update of a proxy,
    Updates should occur periodically, ex. hourly, every 2 hours, twice a day, daily
    '''

    __tablename__ = 'updates'

    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()), unique=True)
    pid = Column(String(length=255), ForeignKey('proxies.id'), nullable=False)
    ts = Column(BigInteger, nullable=False) # Unix-Timestamp
    latency = Column(Integer(), nullable=False) # Latency in ms

    def __repr__(self):
        return f'Update(id={self.id}, pid={self.pid}, ts={self.ts}, latency={self.latency})'