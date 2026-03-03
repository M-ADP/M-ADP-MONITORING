from src.core.client.requester import Requester
from src.infra.requester.http import HttpRequester


async def get_requester() -> Requester:
    return HttpRequester()