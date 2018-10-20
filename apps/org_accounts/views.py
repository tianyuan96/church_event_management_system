from .forms import RegisterOrganisationForm, LoginOrganisationForm
from .models import OrganisationDetails
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.events.models import Event
from apps.core import views as core_views
from apps.org_accounts import forms
from apps.org_accounts import models
from apps.org_accounts.models import OrganisationDetails
from django.contrib.auth.models import User
from apps.main import forms as mainp_forms
from apps.main import models as mainp_models
from django.contrib import messages
from django.conf import settings
from apps.user_accounts.models import UserDetails


class OrganisationProfileView(LoginRequiredMixin, generic.ListView, core_views.BaseView):

    template_name = "org_accounts/registration/profile.html"
    context_object_name = "events"
    model = Event
    page_title = 'Profile'
    # login_url = '/accounts/organisations/login/'

    def user_details(self):

        return OrganisationDetails.objects.get(user=self.request.user.id)

    def events(self):
        return Event.objects.all()

    def main_page(self):
        main_page,_ = mainp_models.MainPage.objects.get_or_create(name="main_page")
        return mainp_forms.MainPageForm(instance=main_page)





# Create your views here.
class RegisterOrganisationView(generic.FormView, core_views.BaseView):

    form_class = RegisterOrganisationForm
    page_title = "Register Organisation"
    template_name = 'org_accounts/registration/register.html'
    success_url = reverse_lazy('org_accounts:profile')


    # Get the data from the registration form and register the user
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            taken, error = form.username_taken()
            if taken:
                return render(request, self.template_name, {'form': form, 'error': error, })

            user = form.save(commit=False)
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user.set_password(password)
            user.username = username
            user.email = username
            user.is_staff = True # grant staff privilege
            user.save()

            # Store the orgs other details as well
            org = OrganisationDetails(name=form.cleaned_data['organisation'], user=user)
            org.save()

            detail=UserDetails.objects.create(user=user,display_name=form.cleaned_data['organisation'])
            detail.save()
            # Auto log the user in
            user = authenticate(username=username, password=password)

            if user is not None: # if the user was successfully authed
                if user.is_active:  # The user has not been banned
                    login(request, user)
                    print("SUCCESSFULLY CREATED ORGANISATION")
                    return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, })


class LoginOrganisationView(generic.FormView, core_views.BaseView):

    form_class = LoginOrganisationForm
    page_title = "Login"
    template_name = 'org_accounts/registration/login.html'
    success_view = 'org_accounts:profile'
    success_url = reverse_lazy(success_view)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user:
                if user.is_active and user.is_staff and not user.is_superuser:
                    login(request, user)
                    next_page = request.POST.get('next')
                    if next_page and next_page != '':
                        return redirect(next_page)
                    return redirect(self.success_url)

                else:
                    form.errors[""] = " You aren't allowed to log in here"
            else:
                
                form.errors["password"] = ' Wrong email or password'

        # This is very ugly, please never do this
        return render(request, self.template_name, { 'form': form, 'view': {'title': self.page_title, 'project_name': settings.PROJECT_NAME}, })


class LogoutOrganisationView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        response = logout(request)
        return redirect(self.success_url)


class UpdateUserView(generic.View):

    success_url = reverse_lazy('org_accounts:profile')


    def post(self, request, *args, **kwargs):

        user_form = forms.OrgnasationForm(request.POST, instance=request.user)
        valid = user_form.is_valid()
        if not valid:
            messages.add_message(request, messages.ERROR, 'Could not update user details.', extra_tags='danger profile_update')
            return redirect(self.success_url)

        instance = user_form.save()

        # Update user details as well
        display_name = user_form.cleaned_data['display_name']
        models.OrganisationDetails.objects.filter(user=request.user).delete()
        obj, created = models.OrganisationDetails.objects.update_or_create(user=request.user, display_name=display_name)
        messages.add_message(request, messages.INFO, 'User details updated!', extra_tags='success profile_update')
        return redirect(self.success_url)
