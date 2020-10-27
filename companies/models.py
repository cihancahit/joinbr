import random
from random import randint

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import mark_safe
from django.contrib.contenttypes.fields import GenericRelation
from users.models import UserProfileModel, User
from ckeditor_uploader.fields import RichTextUploadingField

from custom.custom_tools import get_company_logo_path, get_companyproduct_img_path

from reviews_and_rating.models import ReviewModel, RatingModel
from custom.custom_tools2 import slugify, strip_accents, remove_special
from hitcount.models import HitCountMixin, HitCount
from meta.models import ModelMeta
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Markets(models.Model):
    market_name = models.CharField(max_length=255, verbose_name="Market Name:")

    class Meta:
        verbose_name = 'Market'
        verbose_name_plural = 'Markets'

    def __str__(self):
        return self.market_name


class CompanyTypes(models.Model):
    name = models.CharField(max_length=255, verbose_name="Company Type Name:")

    class Meta:
        verbose_name = 'Company Type'
        verbose_name_plural = 'Company Types'

    def __str__(self):
        return self.name


class CompanyAddress(models.Model):
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name='Location')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name='City')
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name='Country')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        final_loc = ''
        if self.location:
            loc = self.location
            final_loc = loc

        if self.city:
            city = self.city
            final_loc = final_loc + ', ' + city

        if self.country:
            country = self.country
            final_loc = final_loc + ', ' + country
        return final_loc


class Company(ModelMeta, models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name="Company Name")
    single_info = models.CharField(
        null=True,
        blank=True,
        max_length=250,
    )
    info = RichTextUploadingField(
        null=True,
        blank=True, verbose_name="Company Info")
    company_logo = models.ImageField(null=True, upload_to=get_company_logo_path, blank=True,
                                     verbose_name="Company Logo")
    markets = models.ManyToManyField(Markets, blank=True)
    type = models.ManyToManyField(CompanyTypes, blank=True)
    founded = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    location = models.ManyToManyField(CompanyAddress)
    # location = models.TextField(null=True, blank=True)
    # city = models.TextField(null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    website = models.URLField(
        max_length=100,
        verbose_name='Website',
        null=True,
        blank=True
    )
    avg_rating = models.FloatField(null=True, blank=True, default=80)
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    ratings = GenericRelation(RatingModel, related_query_name='company')
    reviews = GenericRelation(ReviewModel, related_query_name='company')
    follower_list = models.ManyToManyField(UserProfileModel, blank=True)
    linkedin_url = models.CharField(max_length=255, blank=True, null=True)
    facebook_url = models.CharField(max_length=255, blank=True, null=True)
    twitter_url = models.CharField(max_length=255, blank=True, null=True)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    premium = models.BooleanField(
        default=False,
    )
    startup = models.BooleanField(
        default=False,
    )
    size = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    contact_email = models.EmailField(
        null=True,
        blank=True,
    )
    contact_number = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )
    thumbnail100x100 = ImageSpecField(source='company_logo', processors=[ResizeToFill(100, 100)], format="PNG",
                                      options={'quality': 60})

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    def get_experts(self, slug):
        return self.expert_set.exclude(slug=slug)

    def get_image_thumbnail(self):

        if self.company_logo:
            return mark_safe(
                "<img class='single-com-image' src='" + self.company_logo.url + "' alt='" + self.name + "' />")
        else:
            return mark_safe(
                "<img class='single-com-image' src='/static/assets/images/no_photo.png' alt='" + self.name + "' />")

    get_image_thumbnail.short_description = 'Company Logo'

    company_logo.allow_tags = True

    def get_image_thumbnail_ep(self):

        if self.company_logo:
            return mark_safe(
                "<img class='company-logo' src='" + self.company_logo.url + "' style='width:50px;height:50px' alt='" + self.name + "' />")
        else:
            return mark_safe(
                "<img src='/static/assets/images/no_photo.png' alt='" + self.name + "' />")

    get_image_thumbnail_ep.short_description = 'Company Logo'

    company_logo.short_description = "Article Photo"
    company_logo.allow_tags = True

    def get_image_thumbnail_d(self):

        if self.company_logo:
            return mark_safe(
                "<img src='%s' class='cod-profile-pic' alt='image' />" % self.company_logo.url)
        else:
            return mark_safe(
                "<img class='cod-profile-pic' src='/static/assets/images/no_photo.png' "
                "alt='image' />")

    get_image_thumbnail.short_description = 'Company Logo'

    company_logo.short_description = "Article Photo"
    company_logo.allow_tags = True

    _metadata = {
        'title': 'name',
        'description': 'info',
        'image': 'get_meta_image',
    }

    def get_meta_image(self):
        if self.company_logo:
            return self.company_logo.url

    def save(self, *args, **kwargs):
        slug1 = strip_accents(self.name)
        slug1 = remove_special(slug1)
        slug1 = slug1.lower()[:150]
        # if Company.objects.filter(slug=slug1).exists():
        #     self.slug = slug1 + "_" + str(random.randint(1, 9999))
        self.slug = slug1
        super(Company, self).save(*args, **kwargs)


def random_premium_company():
    sponsored_events = Company.objects.filter(premium=True).values('pk')
    if sponsored_events:
        pk = randint(1, len(sponsored_events)) - 1
        pk = sponsored_events[pk]['pk']
        return Company.objects.filter(pk=pk)


class CompanyProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name:")
    description = RichTextUploadingField(
        null=True,
        blank=True, verbose_name="Product Info")
    img = models.ImageField(null=True, upload_to=get_companyproduct_img_path, blank=True,
                            verbose_name="Product Image")
    company = models.ManyToManyField(Company)
    avg_rating = models.FloatField(null=True, blank=True, default=0)
    cdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ratings = GenericRelation(RatingModel, related_query_name='product')
    reviews = GenericRelation(ReviewModel, related_query_name='product')

    class Meta:
        verbose_name = 'Company Product'
        verbose_name_plural = 'Company Products'

    def __str__(self):
        return self.name
