from abc import ABC, abstractmethod
from typing import Dict, Any


class Requester(ABC):

    @abstractmethod
    async def get(
            self,
            url : str,
            headers : Dict[str, Any] = None,
            params : Dict[str, Any] = None,
            cookies : Dict[str, Any] = None,
    ):
        raise NotImplementedError