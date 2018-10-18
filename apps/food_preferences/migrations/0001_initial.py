# Generated by Django 2.1 on 2018-10-18 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vegetarian', models.BooleanField(default=False)),
                ('vegan', models.BooleanField(default=False)),
                ('nut_allergy', models.BooleanField(default=False)),
                ('egg_allergy', models.BooleanField(default=False)),
                ('dairy_allergy', models.BooleanField(default=False)),
                ('soy_allergy', models.BooleanField(default=False)),
                ('shellfish_allergy', models.BooleanField(default=False)),
                ('fish_allergy', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=300)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
