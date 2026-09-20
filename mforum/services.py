from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from django.shortcuts import redirect, render

if TYPE_CHECKING:
    from django import forms
    from django.http import HttpRequest, HttpResponse


@dataclass
class ServiceResponse:
    template_name: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    redirect_to: str = ""
    status: HTTPStatus = HTTPStatus.OK


class BaseService(ABC):
    """Marker base for the app/services/*.py convention: one file per action.
    Concrete services are callables; most will want BaseRenderService below
    rather than implementing __call__ from scratch."""

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


class BaseRenderService(BaseService, ABC):
    """A service that validates its input through a plain Django Form and renders
    a template or issues a redirect. Views stay thin and just do
    `SomeService(request, data=data)()`."""

    form_class: type[forms.BaseForm] | None = None

    def __init__(self, request: HttpRequest, /, *, data: dict[str, Any] | None = None) -> None:
        self.request = request
        self.form: forms.BaseForm | None = self.form_class(data) if self.form_class is not None else None

    @property
    def cleaned_data(self) -> dict[str, Any]:
        return self.form.cleaned_data if self.form is not None else {}

    @abstractmethod
    def handle(self) -> ServiceResponse: ...

    def handle_invalid(self) -> ServiceResponse:
        raise NotImplementedError()

    def __call__(self) -> HttpResponse:
        if self.form is not None and not self.form.is_valid():
            service_response = self.handle_invalid()
        else:
            service_response = self.handle()

        if service_response.redirect_to:
            return redirect(service_response.redirect_to)

        return render(
            self.request,
            service_response.template_name,
            service_response.context,
            status=service_response.status,
        )
