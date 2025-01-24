from pydantic import BaseModel
from typing import Optional
from model.data_classes import (
    ProtocolEnum,
    CountryEnum
)

class Proxy_Filter_Schema(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[ProtocolEnum] = None
    anonymity: Optional[bool] = None
    country: Optional[CountryEnum] = None
    
    min_latency: Optional[int] = None
    max_latency: Optional[int] = None

    ip_score: Optional[str] = None
    active: Optional[bool] = None

class Proxy_Schema(BaseModel):
    host: str
    port: int
    protocol: ProtocolEnum
    anonymity: Optional[bool]
    country: Optional[CountryEnum]
    latency: Optional[int]
    secret: Optional[str]
    last_ts: Optional[int]
    ip_score: Optional[str]
    active: Optional[bool]

class Update_Schema(BaseModel):
    pid: str
    ts: int
    latency: int