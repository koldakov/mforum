from django.urls import path
from django.views.generic import RedirectView

from accounts import views

app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        views.register,
        name="register",
    ),
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "settings/",
        RedirectView.as_view(pattern_name="accounts:settings_general"),
        name="settings",
    ),
    path(
        "settings/general/",
        views.settings_general,
        name="settings_general",
    ),
    path(
        "settings/security/",
        views.settings_security,
        name="settings_security",
    ),
]
