# Generated by Django 2.2.1 on 2020-01-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fec_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'verbose_name': 'Email List',
                'verbose_name_plural': 'Emails',
            },
        ),
    ]