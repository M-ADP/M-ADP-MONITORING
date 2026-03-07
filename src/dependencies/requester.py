from src.core.client.requester import Requester
from src.infra.requester.http import HttpRequester


def get_requester() -> Requester:
    return HttpRequester()