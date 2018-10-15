from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.urls import reverse_lazy


class BaseView():
    page_title = "Title"


    def title(self):
        return self.page_title

    def project_name(self):
        return settings.PROJECT_NAME

    def profile_page(self):

        user = self.request.user

        if user.is_staff:
            return reverse_lazy('org_accounts:profile')
        else:
            return reverse_lazy('user_accounts:profile')

    def logout_page(self):

        user = self.request.user

        if user.is_staff:
            return reverse_lazy('org_accounts:logout')
        else:
            return reverse_lazy('user_accounts:logout')
