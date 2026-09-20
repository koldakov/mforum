from django.contrib.auth import get_user_model, login

from accounts.forms import RegisterForm
from mforum.services import BaseRenderService, ServiceResponse

User = get_user_model()


class RegisterService(BaseRenderService):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def handle(self) -> ServiceResponse:
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password2"],
        )
        login(self.request, user)
        return ServiceResponse(redirect_to="forum:index")

    def handle_invalid(self) -> ServiceResponse:
        return ServiceResponse(
            template_name=self.template_name,
            context={
                "form": self.form,
            },
        )
