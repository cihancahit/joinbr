# Generated by Django 2.2.1 on 2020-02-22 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0007_auto_20200206_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertevents',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='expert.ExpertTags'),
        ),
    ]
