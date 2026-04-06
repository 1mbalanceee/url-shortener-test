from pydantic import BaseModel, HttpUrl, ConfigDict

class ShortenRequest(BaseModel):
    url: HttpUrl

class ShortenResponse(BaseModel):
    short_id: str

class StatsResponse(BaseModel):
    short_id: str
    original_url: str
    clicks: int

    model_config = ConfigDict(from_attributes=True)
