# Generated by Django 5.2.3 on 2025-07-01 19:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_event_semester_eventoccurence'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='pages.semester'),
        ),
    ]
