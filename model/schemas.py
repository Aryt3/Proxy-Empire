from pydantic import BaseModel
from typing import Optional
from model.data_classes import (
    ProtocolEnum,
    CountryEnum
)

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
