from django.db import models

from users.models import User


class Organizer(models.Model):
    name = models.CharField(
        max_length=250,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name


class OrganizerEventsPhotos(models.Model):
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Past Events Photo'
        verbose_name_plural = 'Past Events Photos'


class OrganizerSubscribers(models.Model):
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        null=False
    )

    class Meta:
        verbose_name = 'Organizer Subscriber'
        verbose_name_plural = 'Organizer Subscribers'

    def __str__(self):
        return self.email
