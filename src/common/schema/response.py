from datetime import datetime
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel


class TrafficPointResponse(BaseModel):
    timestamp: datetime
    value: float


class TrafficResponse(BaseModel):
    start: datetime
    end: datetime
    series: list[TrafficPointResponse] = []


T = TypeVar('T')

class MadpResponse(BaseModel, Generic[T]):
    data : Optional[T] = None
    message : Optional[str] = None
