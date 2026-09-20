from forum.models import Category
from mforum.services import BaseRenderService, ServiceResponse


class IndexService(BaseRenderService):
    def handle(self) -> ServiceResponse:
        return ServiceResponse(
            template_name="forum/index.html",
            context={"categories": Category.objects.all()},
        )
