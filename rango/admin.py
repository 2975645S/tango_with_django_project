from django.contrib.admin import ModelAdmin, site
from rango.models import Category, Page, UserProfile


class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


site.register(Category, CategoryAdmin)


class PageAdmin(ModelAdmin):
    list_display = ("title", "category", "url")


site.register(Page, PageAdmin)

site.register(UserProfile)
