# Generated by Django 2.2.1 on 2020-04-10 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='contact_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='single_info',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
