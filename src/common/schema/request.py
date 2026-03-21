from datetime import datetime, timedelta

from fastapi import Query
from pydantic import BaseModel, model_validator

class TrafficRangeRequest(BaseModel):
    start: datetime = Query(
        default_factory=lambda: datetime.now() - timedelta(hours=1)
    )
    end: datetime = Query(
        default_factory=datetime.now
    )

    @model_validator(mode="after")
    def validate_range(self):
        if self.end <= self.start:
            raise ValueError("start가 end보다 늦은 시점입니다.")
        return self

