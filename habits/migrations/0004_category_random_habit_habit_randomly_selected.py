# Generated by Django 5.1.3 on 2024-11-29 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_category_alarm_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='random_habit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='randomly_selected_category', to='habits.habit'),
        ),
        migrations.AddField(
            model_name='habit',
            name='randomly_selected',
            field=models.BooleanField(default=False),
        ),
    ]
