# Generated by Django 2.1 on 2018-10-01 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='involvedevent',
            old_name='eventId',
            new_name='event',
        ),
    ]