from pydantic import BaseModel
from model.data_classes import (
    ProtocolEnum,
    CountryEnum
)

class Proxy_Schema(BaseModel):
    host: str
    port: int
    protocol: ProtocolEnum
    anonymity: bool
    country: CountryEnum
    latency: int
    secret: str
    last_ts: int
    ip_score: str
    active: bool
