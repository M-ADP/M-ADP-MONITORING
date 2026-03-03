from datetime import datetime

from pydantic import BaseModel


class TrafficResponse(BaseModel):
    start: datetime
    end: datetime

