# from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

from custom.custom_tools import get_profile_img_path,slugify
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth import password_validation

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self):
        return "/users/%i/" % self.pk

    def get_expert_slug(self):
        return self.expert_set.get(user=self).slug

    def get_expert_name(self):
        return self.expert_set.get(user=self).name

    def get_expert_profile_pic(self):
        return self.expert_set.get(user=self).get_profile_pic_url()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
        if not UserProfileModel.objects.filter(user=self):
            UserProfileModel.objects.create(user=self)


class UserRSS(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    rss_link = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'User RSS'
        verbose_name_plural = 'User RSS'

    def __str__(self):
        return self.title


class UserProfileModel(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='Username'
    )
    phone_number = PhoneNumberField(
        verbose_name='Phone Number',
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=255,
        default='',
        verbose_name='Address',
        null=True,
        blank=True
    )
    job_title = models.CharField(
        max_length=255,
        default='',
        verbose_name='Job Title',
        null=True,
        blank=True
    )
    company_organization = models.CharField(
        max_length=255,
        default='',
        verbose_name='Company/Organization',
        null=True,
        blank=True
    )
    soc_media_twitter = models.URLField(
        max_length=255,
        default='',
        verbose_name='Twitter Profile',
        null=True,
        blank=True
    )
    soc_media_fb = models.URLField(
        max_length=100,
        default='',
        verbose_name='Facebook Profile',
        null=True,
        blank=True
    )
    soc_media_linkedin = models.URLField(
        max_length=100,
        default='',
        verbose_name='Linkedin Profile',
        null=True,
        blank=True
    )
    website = models.URLField(
        max_length=100,
        default='',
        verbose_name='Website',
        null=True,
        blank=True
    )
    img = models.ImageField(
        null=True, 
        upload_to=get_profile_img_path, 
        blank=True,
        verbose_name="User Photo"
    )
    rss = models.ManyToManyField(
        UserRSS,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=150,
        null=True
    )
    country = models.CharField(
        max_length=150,
        null=True,
    )

    def __str__(self):
        return '(user id:'+str(self.user.id)+')'+str(self.user.fullname)

    def get_image_thumbnail(self):

        if self.img:
            return mark_safe(
                "<img src='%s' class='user-profile-img img-fluid' style='width:150px; height:auto' alt='image' />" % self.img.url)
        else:
            return mark_safe(
                "<img style='width:150px; height:auto;' class='user-profile-img' src=" + static('assets/images/user.png') + " alt='image' />")

    get_image_thumbnail.short_description = 'Category Photo'

    img.short_description = "User Photo"
    img.allow_tags = True

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.user.fullname)+str(self.user.id)).lower()
        super(UserProfileModel, self).save(*args, **kwargs)
