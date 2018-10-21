import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command
from django.contrib.auth.models import User
from apps.org_accounts.models import OrganisationDetails
from apps.user_accounts.models import UserDetails
from apps.events.models import Event, Post

import loremipsum

class Command(BaseCommand):
    help = 'Shortcut for running the development server'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        # Remove old test data
        call_command('resetdb')

        # host = User.objects.get(email='a@a.com')
        host = User(email='samscheding@gmail.com', username='samscheding@gmail.com')
        host.set_password('password')
        host.save()

        details = UserDetails(user=host, display_name="Sam")

        for i in range(0, 12):
            name = "Auto Generated Event {}".format(i)
            date = datetime.now() + timedelta(days=i)

            description = ''.join(loremipsum.get_sentences(15))
            event = Event(name=name, description=description, location="UNSW", host=host, date=date)
            event.save()


            # Create a toplevel post
            post_text = ''.join(loremipsum.get_sentences(15))
            post = Post(author=host, eventID=event, date=date, message=post_text)
            post.save()

            # Generate some replies
            for j in range(0, 10):
                reply_text = ''.join(loremipsum.get_sentences(5))
                post = Post(author=host, eventID=event, date=date, message=reply_text)
                post.save()
