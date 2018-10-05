from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template

# 3rd Party Libraries
import multitasking

# Custom Django Code
from apps.core import views as core_views

class ConfirmationEmail(core_views.BaseView):

    template_name = "confirmation_email.html"
    subject = "Confirm Your Email"

    @multitasking.task  # This is a decorator that turns send() into a non-blocking method
    def send(self, email, code):

        confirmation_url = '{}/user_confirm/{}'.format(settings.HOSTNAME, code)
        context = {
            'view': self,
            'confirmation_url': confirmation_url,
        }
        message = render_to_string(self.template_name, context)
        to_list = [email]
        send_mail(self.subject, message, settings.EMAIL_HOST_USER, to_list, fail_silently=False)
