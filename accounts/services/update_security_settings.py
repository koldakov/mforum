from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _

from accounts.forms import SecuritySettingsForm
from mforum.services import BaseRenderService, ServiceResponse

if TYPE_CHECKING:
    from django.http import HttpRequest


class UpdateSecuritySettingsService(BaseRenderService):
    form_class = SecuritySettingsForm
    template_name = "accounts/settings_security.html"

    def __init__(self, request: HttpRequest, /, *, data: dict[str, Any] | None = None) -> None:
        self.request = request
        self.form: SecuritySettingsForm = self.form_class(data, user=request.user)

    def handle(self) -> ServiceResponse:
        user = self.request.user
        user.set_password(self.cleaned_data["new_password2"])
        user.save(update_fields=["password"])
        update_session_auth_hash(self.request, user)

        messages.success(self.request, _("Your password has been updated."))
        return ServiceResponse(redirect_to="accounts:settings_security")

    def handle_invalid(self) -> ServiceResponse:
        return ServiceResponse(
            template_name=self.template_name,
            context={
                "form": self.form,
                "active_tab": "security",
            },
        )
