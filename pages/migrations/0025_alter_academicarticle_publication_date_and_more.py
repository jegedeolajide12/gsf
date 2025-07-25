# Generated by Django 5.2.3 on 2025-07-06 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0024_educationalmaterial_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicarticle',
            name='publication_date',
            field=models.DateTimeField(blank=True, help_text='Date of publication', null=True),
        ),
        migrations.CreateModel(
            name='MotivationalWriteup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=200)),
                ('quote', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('for_workers', models.BooleanField(default=False)),
                ('visibility', models.CharField(choices=[('published', 'Published (Visible to everyone)'), ('workers', 'Workers Only'), ('draft', 'Draft (Not visible to anyone)')], default='published', help_text='Who can see this article?', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writeups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
