from typing import TYPE_CHECKING

from django.views.decorators.http import require_http_methods

from accounts.services.login import LoginService
from accounts.services.logout import LogoutService
from accounts.services.register import RegisterService

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
    service: RegisterService = RegisterService(request, data=request.POST or None)
    return service()


def login_view(request: HttpRequest) -> HttpResponse:
    service: LoginService = LoginService(request, data=request.POST or None)
    return service()


@require_http_methods(["POST"])
def logout_view(request: HttpRequest) -> HttpResponse:
    service: LogoutService = LogoutService(request)
    return service()
