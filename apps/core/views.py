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
            return reverse_lazy('org_profile')  # TODO: Give org_accounts a namespace and appname so this can change to match user_accounts
        else:
            return reverse_lazy('user_accounts:user_profile')

    def logout_page(self):

        user = self.request.user

        if user.is_staff:
            return reverse_lazy('org_logout')
        else:
            return reverse_lazy('user_accounts:user_logout')
