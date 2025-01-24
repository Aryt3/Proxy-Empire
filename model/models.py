from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class Proxy(Base):

    __tablename__ = 'proxies'

    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()), unique=True) 
    host = Column(String(length=255)) 
    port = Column(Integer()) 
    protocol = Column(String(length=255)) 
    anonymity = Column(String(length=255)) 
    country = Column(String(length=255)) 
    latency = Column(Integer()) # Latency in ms
    secret = Column(String(length=255))
    last_ts = Column(Integer())
    ip_score = Column(String(length=255))
    active = Column(Boolean())

    def __repr__(self):
        return f'Proxy(id={self.id}, host={self.host}, port={self.port}, protocol={self.protocol}, anonymity={self.anonymity}, country={self.country}, latency={self.latency}, secret={self.secret}, last_ts={self.last_ts}, ip_score={self.ip_score}, active={self.active})'


class Update(Base):

    __tablename__ = 'updates'

    id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()), unique=True)
    pid = Column(String(length=255), ForeignKey('proxies.id'))
    ts = Column(BigInteger) # Unix-Timestamp
    latency = Column(Integer()) # Latency in ms

    def __repr__(self):
        return f'Update(id={self.id}, pid={self.pid}, ts={self.ts}, latency={self.latency})'