# Generated by Django 5.1.5 on 2025-02-20 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_history_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='target_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
