# Generated by Django 2.2.1 on 2020-04-14 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20200414_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='test',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]