# Generated by Django 2.1 on 2018-09-24 07:53

import apps.surveys.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='optioninsurvey',
            name='imageFile',
            field=models.ImageField(blank=True, null=True, upload_to=apps.surveys.models.get_image_path),
        ),
    ]
