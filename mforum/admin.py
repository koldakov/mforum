from django.contrib import admin
from django.contrib.admin import AdminSite as _AdminSite
from django.utils.translation import gettext_lazy

from mforum._env_settings import env_settings
from utils import config


class AdminSite(_AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy(f"{config['project']['name']} admin")

    # Text to put in each page's <div id="site-name">.
    site_header = gettext_lazy(f"{config['project']['name']} administration")

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy(f"{config['project']['name']} administration")

    # URL for the "View site" link at the top of each admin page.
    site_url = env_settings.site_url


admin_site = AdminSite()

for model, model_admin in admin.site._registry.items():
    admin_site.register(model, model_admin.__class__)
