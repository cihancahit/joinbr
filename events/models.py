import uuid
from decimal import Decimal

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.fields import GenericRelation

from languages.fields import LanguageField

from custom.custom_tools import get_event_img_path, get_category_img_path
from companies.models import Company
from custom.custom_tools2 import remove_special
from organizer.models import Organizer
from reviews_and_rating.models import ReviewModel
from users.models import UserProfileModel
from hitcount.models import HitCountMixin, HitCount
from random import randint
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class EventSponsors(models.Model):
    name = models.CharField(
        max_length=100,
        null=True
    )
    url = models.CharField(
        max_length=255,
        null=True
    )
    img = models.ImageField(
        null=True,
        upload_to=get_category_img_path,
        blank=True,
        verbose_name="Sponsor Photo"
    )

    class Meta:
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'

    def __str__(self):
        return self.name

    def get_image_thumbnail(self):

        if self.img:
            return mark_safe(
                "<img src='%s' alt='image' />" % self.img.url)
        else:
            return mark_safe(
                "<img src='/static/assets/images/no_photo.png' alt='" + self.name + "' />")

    get_image_thumbnail.short_description = 'Sponsor Image'

    img.short_description = "Sponsor Image"
    img.allow_tags = True


class Tags(models.Model):
    tag_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        null=True
    )
    img = models.ImageField(
        null=True,
        upload_to=get_category_img_path,
        blank=True,
        verbose_name="Category Photo"
    )
    thumbnail255x140 = ImageSpecField(source='img', processors=[ResizeToFill(255, 140)], format="PNG",
                                      options={'quality': 60})
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=100
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_image_thumbnail(self):

        if self.img:
            return mark_safe(
                "<img src='%s' class='category-detail-pic img-fluid' style='width:850px; height:480px' alt='image' />" % self.img.url)
        else:
            return mark_safe(
                "<img src='/static/assets/images/no_photo.png' alt='" + self.name + "' />")

    get_image_thumbnail.short_description = 'Category Photo'

    img.short_description = "Category Photo"
    img.allow_tags = True

    def save(self, *args, **kwargs):
        self.slug = self.name
        self.slug = remove_special(self.slug)
        self.slug = self.slug.replace(" ", "_")
        self.slug = self.slug.lower()
        super(Category, self).save(*args, **kwargs)


class TicketType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'TicketType'
        verbose_name_plural = 'TicketTypes'

    def __str__(self):
        return self.name


application_choices = [
    ('100', 'By Email'),
    ('200', 'On our website Form'),
]


class Event(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Event Name"
    )
    info = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name="Event Description"
    )
    event_img = models.ImageField(
        null=True,
        upload_to=get_event_img_path,
        blank=True,
        verbose_name="Event Photo"
    )
    start_event_dt = models.DateTimeField(
        auto_now_add=False,
        verbose_name="Start Time"
    )
    finish_event_dt = models.DateTimeField(
        auto_now_add=False,
        verbose_name="Finish Time"
    )
    location = models.CharField(
        null=True,
        blank=True,
        max_length=255)
    city = models.CharField(
        null=True,
        blank=True,
        max_length=255)
    country = models.CharField(
        null=True,
        blank=True,
        max_length=255)
    # speaker field replace by ExpertEvenets model
    # speaker = models.ManyToManyField(
    #     Expert,
    #     blank=True,
    #     related_name='expert'
    # )
    category = models.ManyToManyField(
        Category,
        blank=True,
    )
    ticket_type = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    language = LanguageField(
        null=True
    )
    price = models.DecimalField(
        null=True,
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    quantity = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    sponsored = models.BooleanField(
        null=True,
        default=False
    )
    sponsor = models.ManyToManyField(
        EventSponsors,
        blank=True
    )
    refund_days = models.IntegerField(
        default=0,
        verbose_name="How many days before Event",
        null=True,
    )
    percentage = models.IntegerField(
        default=0,
        verbose_name="Refund Percentage",
        null=True,
    )
    cdate = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        default=uuid.uuid1,
        max_length=150
    )
    follower_list = models.ManyToManyField(
        UserProfileModel,
        blank=True,
        related_name="followed_events",
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    featured = models.BooleanField(
        default=False,
    )
    reviews = GenericRelation(
        ReviewModel,
        related_query_name='event'
    )
    organizer = models.ManyToManyField(
        Organizer,
        related_name='events',
    )
    tag = models.ManyToManyField(
        Tags,
        blank=True,
    )
    ticket_url = models.URLField(
        null=True
    )
    refund_policy_url = models.URLField(
        null=True
    )
    no_refund = models.BooleanField(
        default=False,
    )
    contact_email = models.EmailField(
        null=True,
    )
    speaker_submission = models.BooleanField(
        default=False,
    )
    submission_details = models.TextField(
        null=True,
    )
    application_type = models.BooleanField(
        default=False,
    )
    submission_web_site = models.URLField(
        null=True,
    )
    source_website = models.URLField(
        null=True,
    )
    test = models.CharField(
        max_length=12,
        null=True,
        blank=True,
    )
    thumbnail320x197 = ImageSpecField(source='event_img', processors=[ResizeToFill(320, 197)], format="PNG",
                                      options={'quality': 60})

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name

    def get_image_thumbnail(self):

        if self.event_img:
            return mark_safe(
                "<img src='"+self.event_img.url+"' alt='"+self.name+"' />")
        else:
            return mark_safe(
                "<img src='/static/assets/images/no_photo.png' alt='"+self.name+"' />")

    get_image_thumbnail.short_description = 'Event Photo'

    event_img.short_description = "Event Photo"
    event_img.allow_tags = True

    def get_image_thumbnail_admin(self):

        if self.event_img:
            return mark_safe(
                "<img src='"+self.event_img.url+"' class='event-detail-pic img-fluid' style='width:100px; height:100' alt='"+self.name+"'/>")
        else:
            return mark_safe(
                "<img src='/static/assets/images/no_photo.png' alt='"+self.name+"' />")

    get_image_thumbnail.short_description = 'Event Photo'

    event_img.short_description = "Event Photo"
    event_img.allow_tags = True


def random_premium_event():
    sponsored_events = Event.objects.filter(sponsored=True).values('pk')
    if sponsored_events:
        pk = randint(1, len(sponsored_events)) - 1
        pk = sponsored_events[pk]['pk']
        return Event.objects.filter(pk=pk)


class Ticket(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        null=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Ticket Name"
    )
    description = models.TextField(
        null=True, blank=True,
        max_length=255
    )
    active = models.BooleanField(
        default=True,
        verbose_name=("Active"),
    )
    price = models.DecimalField(
        null=True,
        max_digits=7, decimal_places=2,
    )
    quota_left = models.DecimalField(
        null=True,
        max_digits=7, decimal_places=0,
    )
    ticket_type = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    class Meta:
        verbose_name = ("Ticket")
        verbose_name_plural = ("Tickets")

    def __str__(self):
        return self.name


class AggrEvents(models.Model):
    name = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    location = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    img = models.ImageField(
        null=True,
        upload_to=get_event_img_path,
        blank=True,
        verbose_name="Event Photo"
    )
    startdate = models.DateTimeField(
        null=True,
        blank=True,
    )
    enddate = models.DateTimeField(
        null=True,
        blank=True,
    )
    source = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    content = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name="Event Description"
    )
    company = models.ManyToManyField(Company)
    bg_color = models.CharField(max_length=7, default='#fff')
    is_approved = models.BooleanField(
        default=False,
        blank=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        default=uuid.uuid1,
        max_length=150
    )

    def get_image_thumbnail(self):

        if self.img:
            return mark_safe(
                "<img src='%s' class='event-detail-pic img-fluid' style='width:100px; height:100' alt='image' />" % self.img.url)
        else:
            return mark_safe(
                "<img src='https://crestaproject.com/demo/nucleare-pro/wp-content/themes/nucleare-pro/images/no-image"
                "-box.png' alt='image' />")

    get_image_thumbnail.short_description = 'Event Photo'

    img.short_description = "Event Photo"
    img.allow_tags = True

    class Meta:
        verbose_name = 'AggrEvent'
        verbose_name_plural = 'AggrEvents'

    def __str__(self):
        return self.name
