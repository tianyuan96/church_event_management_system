# Generated by Django 2.1 on 2018-09-12 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20180912_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='optioninsurvey',
            name='name',
            field=models.CharField(default='option1', max_length=50),
        ),
    ]
