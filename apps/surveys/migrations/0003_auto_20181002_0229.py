# Generated by Django 2.1 on 2018-10-02 02:29

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_optioninsurvey_imagefile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optioninsurvey',
            name='description',
            field=ckeditor.fields.RichTextField(default='option1', max_length=100),
        ),
    ]
