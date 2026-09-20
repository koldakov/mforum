from django.contrib.auth import logout

from mforum.services import BaseRenderService, ServiceResponse


class LogoutService(BaseRenderService):
    def handle(self) -> ServiceResponse:
        logout(self.request)
        return ServiceResponse(redirect_to="forum:index")
