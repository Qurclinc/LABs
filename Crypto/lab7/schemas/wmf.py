from pydantic import BaseModel

class ExchangeData(BaseModel):
    generated_key: str
    
class InitiateData(BaseModel):
    from_username: str
    to_username: str
    secret_key: str
    timestamp: float

class Message(BaseModel):
    text: str
    timestamp: float