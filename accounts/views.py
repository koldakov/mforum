from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from accounts.services.login import LoginService
from accounts.services.logout import LogoutService
from accounts.services.register import RegisterService
from accounts.services.update_general_settings import UpdateGeneralSettingsService
from accounts.services.update_security_settings import UpdateSecuritySettingsService

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


@login_required
def settings_general(request: HttpRequest) -> HttpResponse:
    service: UpdateGeneralSettingsService = UpdateGeneralSettingsService(request, data=request.POST or None)
    return service()


@login_required
def settings_security(request: HttpRequest) -> HttpResponse:
    service: UpdateSecuritySettingsService = UpdateSecuritySettingsService(request, data=request.POST or None)
    return service()
