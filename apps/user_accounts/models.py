from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Confirmations(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=255)
    has_confirmed = models.BooleanField(default=False)

class UserDetails(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_detail")
    display_name = models.CharField(max_length=40)
