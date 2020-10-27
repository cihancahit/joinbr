from django.db import models


# Create your models here.


class Country(models.Model):
    cc_fips = models.CharField(max_length=2, null=True, blank=True, verbose_name="Country FIPS Code")
    cc_iso = models.CharField(max_length=2, null=True, blank=True, verbose_name="Country ISO Code")
    tld = models.CharField(max_length=3, null=True, blank=True, verbose_name="Country TLD Code")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Country Name")

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE,)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="City Name")

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

