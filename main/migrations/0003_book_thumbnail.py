# Generated by Django 5.1.5 on 2025-01-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_book_slug_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]
