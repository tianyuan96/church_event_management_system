# Generated by Django 2.1 on 2018-10-21 11:05

import apps.surveys.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionInSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', ckeditor.fields.RichTextField(blank=True, max_length=100, null=True)),
                ('imageFile', models.ImageField(blank=True, null=True, upload_to=apps.surveys.models.get_image_path)),
                ('vegetarian', models.BooleanField(default=False)),
                ('vegan', models.BooleanField(default=False)),
                ('nut_allergy', models.BooleanField(default=False)),
                ('egg_allergy', models.BooleanField(default=False)),
                ('dairy_allergy', models.BooleanField(default=False)),
                ('soy_allergy', models.BooleanField(default=False)),
                ('shellfish_allergy', models.BooleanField(default=False)),
                ('fish_allergy', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('isClose', models.BooleanField(default=False)),
                ('isFinalized', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.InvolvedEvent')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='UserChoose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.OptionInSurvey')),
                ('participation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.InvolvedEvent')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey')),
            ],
        ),
        migrations.AddField(
            model_name='optioninsurvey',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey'),
        ),
    ]
