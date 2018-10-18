from django.db import models
from django.contrib.auth.models import User

class OrganisationDetails(models.Model):

    display_name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
