# Generated by Django 2.2.1 on 2019-12-25 00:03

import ckeditor_uploader.fields
import custom.custom_tools
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='Availability')),
            ],
            options={
                'verbose_name': 'Availability',
                'verbose_name_plural': 'Availability',
            },
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Expert Name')),
                ('business_title', models.CharField(blank=True, max_length=255, verbose_name='Business Title')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='location')),
                ('country', models.CharField(blank=True, max_length=255, verbose_name='country')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='city')),
                ('bio', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Biography')),
                ('expert_img', models.ImageField(blank=True, null=True, upload_to=custom.custom_tools.get_expert_img_path, verbose_name='Profile Pic')),
                ('is_verified', models.BooleanField(blank=True, default=False)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('linkedin_url', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_url', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_url', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_url', models.CharField(blank=True, max_length=255, null=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('is_approved', models.BooleanField(blank=True, default=False)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('cdate', models.DateTimeField(auto_now_add=True, null=True)),
                ('claimed', models.BooleanField(default=False, null=True)),
                ('avg_rating', models.FloatField(blank=True, default=0, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('availability', models.ManyToManyField(to='expert.Availability')),
                ('company', models.ManyToManyField(blank=True, to='companies.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Expert',
                'verbose_name_plural': 'Experts',
            },
        ),
        migrations.CreateModel(
            name='ExpertTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=255, verbose_name='Expert Tags:')),
            ],
            options={
                'verbose_name': 'Expert Tag',
                'verbose_name_plural': 'Expert Tags',
            },
        ),
        migrations.CreateModel(
            name='ExpertTags1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise_fields', models.CharField(max_length=255, verbose_name='Fields of Experts:')),
            ],
            options={
                'verbose_name': 'Field of Experts',
                'verbose_name_plural': 'Fields of Experts',
            },
        ),
        migrations.CreateModel(
            name='Industries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Industry name')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Industry',
                'verbose_name_plural': 'Industries',
            },
        ),
        migrations.CreateModel(
            name='ExpertEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exxperts', to='expert.Expert')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert.ExpertTags')),
            ],
            options={
                'verbose_name': 'Expert Event',
                'verbose_name_plural': 'Expert Events',
            },
        ),
        migrations.AddField(
            model_name='expert',
            name='fields_of_experties',
            field=models.ManyToManyField(blank=True, to='expert.ExpertTags1', verbose_name='Fields of Expertise'),
        ),
    ]
