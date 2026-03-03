from datetime import datetime, timedelta

from fastapi import Query
from pydantic import BaseModel


class TrafficRangeRequest(BaseModel):
    start: datetime = Query(
        datetime.now()
    )
    end: datetime = Query(
        default_factory=lambda: datetime.now() + timedelta(days=7) # 일주일 뒤
    )

