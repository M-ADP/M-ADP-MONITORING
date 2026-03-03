from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class MetricsClient(ABC):

    @abstractmethod
    async def query(
            self,
            ql: str, # ql = query language
            ts: datetime,
    ) -> Any:
        """단일 시점 쿼리"""
        raise NotImplementedError

    @abstractmethod
    async def query_range(
            self,
            ql: str,
            start: datetime,
            end: datetime,
            step: int,
    ) -> Any:
        """구간 조회"""
        raise NotImplementedError