# Generated by Django 2.1 on 2018-10-20 07:26

import apps.main.models
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='main_page', max_length=20, unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, max_length=512)),
                ('imageFile', models.ImageField(blank=True, null=True, upload_to=apps.main.models.get_image_path)),
            ],
        ),
    ]
