# Generated by Django 5.0 on 2024-01-18 05:06

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_hotel_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
