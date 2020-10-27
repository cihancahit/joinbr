from django.contrib import admin

from .models import *


class RatingAdmin(admin.ModelAdmin):
    list_display = ['content_object', ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['content_title', 'creation_date', ]


admin.site.register(ReviewModel, ReviewAdmin)
admin.site.register(RatingModel, RatingAdmin)
admin.site.register(ReportCategories)
admin.site.register(ReviewReports)
