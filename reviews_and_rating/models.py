# from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import UserProfileModel


class ReviewModel(models.Model):
    """
    Represents a user review, which includes free text and images.

    :reviewed_item: Object, which is reviewed.
    :user: User, which posted the rating.
    :content (optional): Running text.
    :content_title: Title for content.
    :creation_date: The date and time, this review was created.
    :score: Star count
    """
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True
    )
    object_id = models.PositiveIntegerField(
        null=True
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    user = models.ForeignKey(
        UserProfileModel,
        verbose_name='User',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        max_length=1024,
        verbose_name='Content',
        blank=True,
    )
    content_title = models.CharField(
        max_length=40,
        verbose_name='Content Title',
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )
    score = models.FloatField(
        verbose_name='Score',
        default=0,
        null=True,
    )
    anon = models.BooleanField(
        default=False,
    )
    reviewer_name = models.CharField(
        max_length=60,
        verbose_name='Reviewer Name',
        blank=True,
        null=True,
    )
    position = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    tags = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    rating_flag = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class RatingModel(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    excellent = models.FloatField(
        max_length=20,
        default=0
    )
    great = models.FloatField(
        max_length=20,
        default=0
    )
    average = models.FloatField(
        max_length=20,
        default=0
    )
    poor = models.FloatField(
        max_length=20,
        default=0
    )
    bad = models.FloatField(
        max_length=20,
        default=0
    )

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class ReportCategories(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Report Category Title',
                             blank=True, )
    description = models.TextField(
        max_length=1024,
        verbose_name=' Report Category Description',
        blank=True,
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Report Category'
        verbose_name_plural = 'Report Categories'

    def __str__(self):
        return self.title


class ReviewReports(models.Model):
    title = models.CharField(
        max_length=40,
        verbose_name='Report Title',
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=1024,
        verbose_name='Description',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        ReportCategories,
        on_delete=models.CASCADE,
        null=True
    )
    review = models.ForeignKey(
        ReviewModel,
        on_delete=models.CASCADE,
        null=True
    )

