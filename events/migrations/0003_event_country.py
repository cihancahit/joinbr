# Generated by Django 2.2.1 on 2019-12-26 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20191225_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
