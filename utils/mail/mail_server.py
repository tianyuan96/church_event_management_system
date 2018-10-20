# Standard Library
import os

# Django
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string, get_template

# 3rd Party Libraries
import multitasking

class ConfirmationEmail():

    def __init__(self):
        self.host_name = settings.HOSTNAME  # The domain name of the website. In development this would be 127.0.0.1:8000
        self.template_name = "confirmation_email.html"
        self.subject = "Confirm Your Email"
        self.sender = settings.EMAIL_HOST_USER

    @multitasking.task  # This is a decorator that turns send() into a non-blocking method
    def send(self, to_email, code):

        confirmation_url = '{}/user_confirm/{}?email={}'.format(self.host_name, code, to_email)
        context = {
            'confirmation_url': confirmation_url,
        }

        # Supply both html and plaintext content, in case the user's email client doesn't support html
        text_content = "Visit the following url to confirm your Church Bookings account. \n{}".format(confirmation_url)
        html_content = render_to_string(self.template_name, context)
        msg = EmailMultiAlternatives(self.subject, text_content, self.sender, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class ForumReplyEmail():

    def __init__(self):
        self.host_name = settings.HOSTNAME  # The domain name of the website. In development this would be 127.0.0.1:8000
        self.template_name = "forum_reply_email.html"
        self.subject = "New Forum Reply!"
        self.sender = settings.EMAIL_HOST_USER

    @multitasking.task  # This is a decorator that turns send() into a non-blocking method
    def send(self, to_email, event_id):


        forum_link = '{}/event/discussion/{}'.format(self.host_name, event_id)
        context = {
            'forum_link': forum_link,
        }

        # Supply both html and plaintext content, in case the user's email client doesn't support html
        text_content = "Visit the following url to see the new forum reply. \n{}".format(forum_link)
        html_content = render_to_string(self.template_name, context)
        msg = EmailMultiAlternatives(self.subject, text_content, self.sender, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class PostUpdateEmail():

    def __init__(self):
        self.host_name = settings.HOSTNAME  # The domain name of the website. In development this would be 127.0.0.1:8000
        self.template_name = "post_update_email.html"
        self.subject = "A post you are following has been updated!"
        self.sender = settings.EMAIL_HOST_USER

    @multitasking.task  # This is a decorator that turns send() into a non-blocking method
    def send(self, email_list, post_id):

        forum_link = '{}/event/discussion/{}'.format(self.host_name, post_id)
        context = {
            'forum_link': forum_link,
        }

        # Supply both html and plaintext content, in case the user's email client doesn't support html
        text_content = "Visit the following url to see the new forum reply. \n{}".format(forum_link)
        html_content = render_to_string(self.template_name, context)
        msg = EmailMultiAlternatives(self.subject, text_content, self.sender, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
