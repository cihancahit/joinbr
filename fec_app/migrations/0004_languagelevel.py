# Generated by Django 2.2.1 on 2020-03-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fec_app', '0003_auto_20200114_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=30)),
            ],
        ),
    ]
