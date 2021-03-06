# Generated by Django 2.2.1 on 2019-12-25 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc_fips', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country FIPS Code')),
                ('cc_iso', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country ISO Code')),
                ('tld', models.CharField(blank=True, max_length=3, null=True, verbose_name='Country TLD Code')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Country Name')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='City Name')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country.Country')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
    ]
