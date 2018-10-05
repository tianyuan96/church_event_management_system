from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template

# 3rd Party Libraries
import multitasking

# Custom Django Code
from apps.core import views as core_views

"""
    This inherits from some views so that we can leverage the templating stuff to customise emails
"""
class ConfirmationEmail(core_views.BaseView):

    def __init__(self):
        self.host_name = settings.HOSTNAME  # The domain name of the website. In development this would be 127.0.0.1:8000
        self.template_name = "confirmation_email.html"
        self.subject = "Confirm Your Email"
        self.sender = settings.EMAIL_HOST_USER

    @multitasking.task  # This is a decorator that turns send() into a non-blocking method
    def send(self, email, code):

        confirmation_url = '{}/user_confirm/{}'.format(self.host_name, code)
        context = {
            'view': self,
            'confirmation_url': confirmation_url,
        }
        message = render_to_string(self.template_name, context)
        recipients = [email]
        send_mail(self.subject, message, self.sender, recipients, fail_silently=False)
