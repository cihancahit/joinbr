# Generated by Django 2.2.1 on 2020-03-04 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0011_auto_20200304_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expert',
            old_name='complation_percentage',
            new_name='completion_percentage',
        ),
    ]