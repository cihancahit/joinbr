from django.contrib import admin

from .models import ExpertTags1, Expert, Industries, ExpertTags,\
    Availability, ExpertEvents, ExpertTypes, ExpertColleagues, \
    ExpertProfileCompilation, ExpertLanguages


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('get_image_thumbnail', 'business_title', 'name', 'slug')
    filter_horizontal = ('industry', 'company', 'follower_list', 'language', 'fields_of_experties', )
    search_fields = ["name", "bio"]


class ExpertEventAdmin(admin.ModelAdmin):
    list_display = ('expert', 'event', 'tag', 'creation_date')
    autocomplete_fields = ['expert', 'event']


class ExpertColleaguesAdmin(admin.ModelAdmin):
    list_display = ('expert', 'colleague', 'confirmed',)
    autocomplete_fields = ['expert', 'colleague', ]


class ExpertProfileCompilationAdmin(admin.ModelAdmin):
    list_display = ('expert', 'name', 'icon_url',)


class ExpertLanguagesAdmin(admin.ModelAdmin):
    list_display = ('expert', 'language', 'level')


admin.site.register(Expert, ExpertAdmin)
admin.site.register(ExpertTags1)
admin.site.register(ExpertTags)
admin.site.register(Industries)
admin.site.register(Availability)
admin.site.register(ExpertTypes)
admin.site.register(ExpertEvents, ExpertEventAdmin)
admin.site.register(ExpertColleagues, ExpertColleaguesAdmin)
admin.site.register(ExpertProfileCompilation, ExpertProfileCompilationAdmin)
admin.site.register(ExpertLanguages, ExpertLanguagesAdmin)
