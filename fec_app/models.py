from django.db import models


class Languages(models.Model):
    language = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.language


class EmailList(models.Model):
    email = models.CharField(max_length=225, null=True, blank=True)
    email_updates = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self):
        return self.email


class LanguageLevel(models.Model):
    level = models.CharField(
        max_length=30,
    )

    def __str__(self):
        return self.level