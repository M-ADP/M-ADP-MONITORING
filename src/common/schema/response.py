from datetime import datetime
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

class TrafficResponse(BaseModel):
    start: datetime
    end: datetime


T = TypeVar('T')

class MadpResponse(BaseModel, Generic[T]):
    data : Optional[T] = None
    message : Optional[str] = None
