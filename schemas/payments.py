from pydantic import BaseModel

class Subcription(BaseModel):
    plan_name : str
    features: str
    price: float
    
