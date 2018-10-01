from django.shortcuts import render
from django.views import generic
from django.conf import settings


class BaseView():
    page_title = "Title"
    profile_url = ''
    logout_url = ''

    def title(self):
        return self.page_title

    def project_name(self):
        return settings.PROJECT_NAME

    def profile_page(self):
        return self.profile_url

    def logout_page(self):
        return self.logout_url
