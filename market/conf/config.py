from dataclasses import dataclass

@dataclass
class Config:
    token_path: str
    domain: str
    appkey: str
    secretkey: str
    token: str
    market_code: str
    tick_date: str
    start_date: str
    end_date: str
    name: str
    flavor: str

