from django.db import models
from custom.custom_tools import get_news_img_path
from django.utils.html import mark_safe


class Tags(models.Model):
    tag_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag_name


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    article_img = models.ImageField(null=True, upload_to=get_news_img_path, blank=True,
                                    verbose_name="News Photo")
    link = models.CharField(max_length=255, null=True, blank=True)
    img_link = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(Tags)
    publish_date = models.DateTimeField(null=True, blank=True)
    sponsored = models.BooleanField(default=False)
    cdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def get_image_thumbnail(self):
        if self.article_img:
            return mark_safe("<img src='%s' style='width:300px;height:auto' alt='"+self.title+"' />" % self.article_img.url)
        else:
            return mark_safe(
                "<img src='https://crestaproject.com/demo/nucleare-pro/wp-content/themes/nucleare-pro/images/no-image"
                "-box.png' alt='image' />")

    article_img.short_description = "Article Photo"
    article_img.allow_tags = True