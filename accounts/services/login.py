from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _

from accounts.forms import LoginForm
from mforum.services import BaseRenderService, ServiceResponse


class LoginService(BaseRenderService):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def handle(self) -> ServiceResponse:
        assert self.form is not None  # noqa: S101 - form_class is set, so __init__ always builds a form

        user = authenticate(
            self.request,
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
        )
        if user is None:
            self.form.add_error(None, _("Invalid username or password."))
            return ServiceResponse(
                template_name=self.template_name,
                context={"form": self.form},
            )

        login(self.request, user)
        return ServiceResponse(redirect_to="forum:index")

    def handle_invalid(self) -> ServiceResponse:
        return ServiceResponse(
            template_name=self.template_name,
            context={"form": self.form},
        )
