from django.contrib import admin

from forum.models import Category, Post, Topic
from mforum.admin import admin_site


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "position")
    list_editable = ("position",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # noqa: RUF012
    ordering = ("position", "name")


@admin.register(Topic, site=admin_site)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "is_pinned", "is_closed", "created_at")
    list_filter = ("category", "is_pinned", "is_closed")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}  # noqa: RUF012
    autocomplete_fields = ("category", "author")
    ordering = ("-is_pinned", "-created_at")


@admin.register(Post, site=admin_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ("topic", "author", "created_at")
    list_filter = ("topic__category",)
    search_fields = ("body",)
    autocomplete_fields = ("topic", "author")
    ordering = ("-created_at",)
