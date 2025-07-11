# Generated by Django 5.2.3 on 2025-07-09 20:43

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0031_timetable'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyGuides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('thumbnail', models.ImageField(blank=True, help_text='Thumbnail image for the study guide', null=True, upload_to='study-guides/thumbnails/')),
                ('content', models.TextField(help_text='Content of the study guide in Markdown format')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('publication_date', models.DateTimeField(blank=True, help_text='Date of publication', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('for_workers', models.BooleanField(default=False)),
                ('visibility', models.CharField(choices=[('published', 'Published (Visible to everyone)'), ('workers', 'Workers Only'), ('draft', 'Draft (Not visible to anyone)')], default='published', help_text='Who can see this study guide?', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_guides', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text="Tags for the study guide, e.g., 'Bible Study, Faith'", through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Study Guides',
                'ordering': ['-created_at'],
            },
        ),
    ]
