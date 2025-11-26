from datetime import datetime

from  pydantic import BaseModel
class URLCreate(BaseModel):
    original_url: str


class URLInDB(BaseModel):
    short_url: str
    original_url: str
    created_at: datetime
    click_count: int

    model_config = {
        "from_attributes": True
    }

class URLResponse(BaseModel):
    short_url: str

