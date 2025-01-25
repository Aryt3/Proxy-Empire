from pydantic import BaseModel
from typing import Optional
from stores.model.data_classes import (
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
    anonymity: Optional[bool] = None
    country: Optional[CountryEnum] = None
    latency: Optional[int] = None
    secret: Optional[str] = None
    last_ts: Optional[int] = None
    ip_score: Optional[str] = None
    active: Optional[bool] = False
    source: Optional[str] = None

class Update_Schema(BaseModel):
    pid: str
    ts: int
    latency: int

class Proxy_Origin_Schema(BaseModel):
    pid: str
    ts: int
    source: str

class Validator_Schema(BaseModel):
    url: str
    response: str | dict
    content_type: str