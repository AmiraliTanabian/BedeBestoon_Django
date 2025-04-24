from django.contrib import admin
from .models import NewsModel

class NewsModelAdmin(admin.ModelAdmin):
    list_display = ["title", "writer", "is_active", "time"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    prepopulated_fields = {
        "slug" : ("title",)
    }

admin.site.register(NewsModel, NewsModelAdmin)
