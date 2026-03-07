from typing import Dict, Any

from httpx import AsyncClient

from src.core.client.requester import Requester

class HttpRequester(Requester):

    def __init__(
            self,
            timeout: float = 10.0,
            verify: bool = True,
    ):
        self._client = AsyncClient(
            timeout=timeout,
            verify=verify,
        )

    async def get(
            self,
            url: str,
            headers: Dict[str, Any] = None,
            params: Dict[str, Any] = None,
            cookies: Dict[str, Any] = None
    ):
        response = await self._client.get(
            url=url,
            headers=headers,
            params=params,
            cookies=cookies,
        )

        response.raise_for_status()

        return response.json()
