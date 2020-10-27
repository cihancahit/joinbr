from django.contrib import admin

from .models import Languages, EmailList, LanguageLevel


class LangAdmin(admin.ModelAdmin):
    list_display = ('language', 'iso_code', 'is_active')
    search_fields = ["language", "iso_code", ]
    list_editable = ('is_active',)


class LanguageLevelAdmin(admin.ModelAdmin):
    list_display = ('level', )


admin.site.register(Languages, LangAdmin)
admin.site.register(LanguageLevel, LanguageLevelAdmin)
admin.site.register(EmailList)
