from pydantic import BaseModel, Field

class add_notifications(BaseModel):
    message : str
    