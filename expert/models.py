from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField

from custom.custom_tools import get_expert_img_path
from custom.custom_tools2 import strip_accents, remove_special
from companies.models import Company
from hitcount.models import HitCountMixin, HitCount

from fec_app.models import Languages, LanguageLevel

from reviews_and_rating.models import ReviewModel, RatingModel

from events.models import Event
from users.models import UserProfileModel, User


class ExpertTags1(models.Model):
    expertise_fields = models.CharField(max_length=255, verbose_name="Fields of Expertise:")

    class Meta:
        verbose_name = 'Field of Expertise'
        verbose_name_plural = 'Fields of Expertise'

    def __str__(self):
        return self.expertise_fields


class ExpertTags(models.Model):
    tags = models.CharField(
        max_length=255,
        verbose_name="Expert Tags:"
    )

    class Meta:
        verbose_name = 'Expert Tag'
        verbose_name_plural = 'Expert Tags'

    def __str__(self):
        return self.tags


class Availability(models.Model):
    CHOICES = [
        ('New opportunities', 'New opportunities'),
        ('Freelancer', 'Freelancer'),
        ('Full Time', 'Full Time'),
    ]
    type = models.CharField(
        max_length=255,
        verbose_name="Availability",
        # choices=CHOICES,
        default='Full Time',
    )

    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availability'

    def __str__(self):
        return self.type


class ExpertTypes(models.Model):
    CHOICES = [
        ('Agencies', 'Agencies'),
        ('Employees', 'Employees'),
    ]
    type = models.CharField(
        max_length=255,
        verbose_name="Expert Type",
        choices=CHOICES,
        default='Employees',
    )

    class Meta:
        verbose_name = 'Expert Type'
        verbose_name_plural = 'Expert Types'

    def __str__(self):
        return self.type


class Industries(models.Model):
    name = models.CharField(max_length=255, verbose_name="Industry name")
    slug = models.SlugField(unique=True, blank=True, max_length=150)

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ", "_")
        super(Industries, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Expert(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name="Expert Name")
    business_title = models.CharField(max_length=255, blank=True, verbose_name="Business Title")
    location = models.CharField(max_length=255, blank=True, verbose_name="location")
    country = models.CharField(max_length=255, blank=True, verbose_name="country")
    city = models.CharField(max_length=255, blank=True, verbose_name="city")
    bio = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name="Biography"
    )
    expert_img = models.ImageField(null=True, upload_to=get_expert_img_path, blank=True,
                                   verbose_name="Profile Pic")
    is_verified = models.BooleanField(default=False, blank=True)
    fields_of_experties = models.ManyToManyField(ExpertTags1, blank=True, verbose_name="Fields of Expertise")
    industry = models.ManyToManyField(Industries, blank=True, verbose_name="Industries")
    score = models.IntegerField(
        null=True,
        blank=True,
        default=0,
    )
    linkedin_url = models.CharField(max_length=255, blank=True, null=True)
    facebook_url = models.CharField(max_length=255, blank=True, null=True)
    twitter_url = models.CharField(max_length=255, blank=True, null=True)
    personal_url = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    language = models.ManyToManyField(Languages, blank=True)
    cdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    company = models.ManyToManyField(Company, blank=True, verbose_name="Company")
    claimed = models.BooleanField(null=True, default=False)
    ratings = GenericRelation(RatingModel, related_query_name='expert')
    reviews = GenericRelation(ReviewModel, related_query_name='expert')
    avg_rating = models.FloatField(null=True, blank=True, default=0)
    follower_list = models.ManyToManyField(UserProfileModel, blank=True, )
    age = models.IntegerField(null=True, blank=True)
    availability = models.ManyToManyField(Availability, blank=True)
    type = models.ManyToManyField(ExpertTypes, blank=True)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    completion_percentage = models.IntegerField(
        default=0
    )
    et_points = models.ImageField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Expert'
        verbose_name_plural = 'Experts'

    def __str__(self):
        return self.name

    def get_profile_pic_url(self):
        if self.expert_img:
            profile_url = self.expert_img.url
        else:
            profile_url = '/static/assets/images/no_photo.png'
        return profile_url

    def get_image_thumbnail(self):

        if self.expert_img:
            return mark_safe("<img class='expert-list-profile-img' src='%s' style='width:140px;height:140px' alt=''/>" % self.expert_img.url)
        else:
            return mark_safe(
                "<img class='expert-list-profile-img' style='width:140px;height:140px' src='/static/assets/images/no_photo.png' alt='image' />")

    def get_image_thumbnail_ed(self):
        if self.expert_img:
            return mark_safe("<img class='exd-profile-img' src='%s' style='width:100px;height:100px' alt='image' />" % self.expert_img.url)
        else:
            return mark_safe(
                "<img class='exd-profile-img' style='width:100px;height:100px' src='/static/assets/images/no_photo.png' alt='image' />")

    expert_img.short_description = "Profile Photo"
    expert_img.allow_tags = True

    def save(self, *args, **kwargs):
        self.slug = strip_accents(self.name)
        self.slug = remove_special(self.slug)
        self.slug = self.slug.lower()[:150]
        super(Expert, self).save(*args, **kwargs)

    def save_2(self, *args, **kwargs):
        self.slug = strip_accents(self.name) + self.slug
        self.slug = remove_special(self.slug)
        self.slug = self.slug.lower()
        if Expert.objects.filter(slug=self.slug).exists():
            self.slug = self.slug + "_" + str(self.id)
        super(Expert, self).save(*args, **kwargs)


class ExpertEvents(models.Model):
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        related_name='exxperts'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='evvents'
    )
    tag = models.ForeignKey(
        ExpertTags,
        on_delete=models.CASCADE,
        null=True,
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    class Meta:
        verbose_name = 'Expert Event'
        verbose_name_plural = 'Expert Events'


class ExpertColleagues(models.Model):
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        null=False,
    )
    colleague = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        related_name='colleague',
    )
    confirmed = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Expert Colleague'
        verbose_name_plural = 'Expert Colleagues'


class ExpertProfileCompilation(models.Model):
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=120,
    )
    icon_url = models.CharField(
        max_length=120,
        default="not_completed.png"
    )

    class Meta:
        verbose_name = 'Expert Profile Compilation'
        verbose_name_plural = 'Expert Profile Compilation'


class ExpertLanguages(models.Model):
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
    )
    language = models.ForeignKey(
        Languages,
        on_delete=models.CASCADE,
    )
    level = models.ForeignKey(
        LanguageLevel,
        on_delete=models.CASCADE,
    )
