# Generated by Django 5.1.5 on 2025-02-24 06:14

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_audiobook_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(default='default', max_length=50),
        ),
        migrations.CreateModel(
            name='Booktranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50)),
                ('translated_title', models.CharField(max_length=255)),
                ('translated_description', models.TextField()),
                ('translated_content', django_ckeditor_5.fields.CKEditor5Field()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='main.book')),
            ],
        ),
    ]
