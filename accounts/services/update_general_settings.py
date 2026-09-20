from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from accounts.forms import GeneralSettingsForm
from mforum.services import BaseRenderService, ServiceResponse

if TYPE_CHECKING:
    from django.http import HttpRequest


class UpdateGeneralSettingsService(BaseRenderService):
    form_class = GeneralSettingsForm
    template_name = "accounts/settings_general.html"

    def __init__(self, request: HttpRequest, /, *, data: dict[str, Any] | None = None) -> None:
        self.request = request
        self.form: GeneralSettingsForm = self.form_class(
            data,
            user=request.user,
            initial={
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            },
        )

    def handle(self) -> ServiceResponse:
        user = self.request.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save(update_fields=["username", "email", "first_name", "last_name"])

        messages.success(self.request, _("Your profile has been updated."))
        return ServiceResponse(redirect_to="accounts:settings_general")

    def handle_invalid(self) -> ServiceResponse:
        return ServiceResponse(
            template_name=self.template_name,
            context={
                "form": self.form,
                "active_tab": "general",
            },
        )
