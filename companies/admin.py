from django.contrib import admin

from .models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('get_image_thumbnail', 'name', 'info')
    filter_horizontal = ['markets', 'type', 'follower_list', 'location']
    search_fields = ["name", "info"]


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyTypes)
admin.site.register(Markets)
admin.site.register(CompanyProduct)
admin.site.register(CompanyAddress)
