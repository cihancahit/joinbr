# Generated by Django 2.2.1 on 2020-03-04 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0008_auto_20200222_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpertProfileCompilation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('icon_url', models.URLField(max_length=120)),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.Expert')),
            ],
        ),
    ]
