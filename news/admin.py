from django.contrib import admin

from .models import News, Tags


# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('get_image_thumbnail', 'title', 'content')




admin.site.register(News,NewsAdmin)
admin.site.register(Tags)