# Generated by Django 2.2.1 on 2020-04-04 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0019_auto_20200331_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='type',
            field=models.CharField(default='Full Time', max_length=255, verbose_name='Availability'),
        ),
    ]