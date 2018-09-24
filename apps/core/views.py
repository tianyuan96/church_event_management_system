from django.shortcuts import render
from django.views import generic
from django.conf import settings

# Create your views here.

class BaseView():
    page_title = "Title"

    def title(self):
        return self.page_title

    def project_name(self):
        return settings.PROJECT_NAME
