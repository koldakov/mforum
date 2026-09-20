from typing import TYPE_CHECKING

from forum.services.index import IndexService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    service: IndexService = IndexService(request)
    return service()
