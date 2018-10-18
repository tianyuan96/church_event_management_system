from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError

from django.views import generic
from django.conf import settings

from apps.user_accounts import forms
from apps.user_accounts import models
from apps.events import models as event_models
from apps.core import views as core_views
from apps.surveys import forms as survey_forms
from apps.surveys import models as survey_models

from apps.food_preferences import forms as pref_forms
from apps.food_preferences import models as pref_models



class UserProfileView(LoginRequiredMixin, generic.TemplateView, core_views.BaseView):

    template_name = "user_accounts/registration/profile.html"
    success_url = reverse_lazy('user_accounts:profile')
    page_title = "Profile"

    """
        The food prefs are defined this way (rather than a view method like below) so that they are
        created in the db the first time the user views their profile.
    """
    def food_preferences(self, queryset=None):
        obj, _ = pref_models.FoodPreferences.objects.get_or_create(user=self.request.user)
        instance = pref_forms.FoodPreferencesForm(instance=obj)

        # We need to add the id here so we can post the form to the correct view
        instance.id = obj.id
        return instance

    """
        Below are attributes that can be rendered in the template, for example {{ view.events }}
    """
    def attending(self):
        # we get the Events here, not the InvolvedEvents, since we need Event data
        return event_models.Event.objects.filter(involvedevent__participant=self.request.user)

    def events(self):
        return event_models.Event.objects.all()

    def update_user_form(self):
        user = self.request.user
        form = forms.UserForm(instance=user)
        user_details = models.UserDetails.objects.get(user=user)
        form.fields['display_name'].initial = user_details.display_name
        return form

class UpdateUserView(generic.View):

    success_url = reverse_lazy('user_accounts:user_profile')


    def post(self, request, *args, **kwargs):

        user_form = forms.UserForm(request.POST, instance=request.user)
        valid = user_form.is_valid()
        if not valid:
            messages.add_message(request, messages.ERROR, 'Could not update user details.', extra_tags='danger profile_update')
            return redirect(self.success_url)

        instance = user_form.save()

        # Update user details as well
        display_name = user_form.cleaned_data['display_name']
        models.UserDetails.objects.filter(user=request.user).delete()
        obj, created = models.UserDetails.objects.update_or_create(user=request.user, display_name=display_name)
        messages.add_message(request, messages.INFO, 'User details updated!', extra_tags='success profile_update')
        return redirect(self.success_url)


class RegisterUserView(generic.FormView, core_views.BaseView):

    form_class = forms.RegisterUserForm
    page_title = "Register"
    template_name = 'user_accounts/registration/register.html'
    #success_url = reverse_lazy('user_profile')
    success_url = reverse_lazy('successfully_registered')
    profile_url = reverse_lazy('user_accounts:profile')

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
            user.save()

            # Auto log the user in
            user = authenticate(username=username, password=password)
            code = hash(username)
            models.Confirmations.objects.create(user=user, confirmation_code=code)
            user_to_confirm = models.Confirmations.objects.get(user=user)
            if user is not None: # if the user was successfully authed
                if user.is_active:  # The user has not been banned
                    login(request, user)
                    if user_to_confirm.has_confirmed is False:



                        subject = 'Please activate your account at ChurchEvent'
                        message = 'Welcome to ChurchEvent!\n Please activate your account at 127.0.0.1:8000/user_confirm/{0}'.format(str(code))
                        from_email = settings.EMAIL_HOST_USER
                        to_list = [username]
                        send_mail(subject, message, from_email, to_list, fail_silently=True)
                        messages.success(request, 'Thank you, we will be in touch')
                        return redirect(self.success_url)
                    else:
                        return redirect(self.profile_url)

        return render(request, self.template_name, {'form': form, })

class NeedActivateView(generic.TemplateView, core_views.BaseView):

    template_name = "user_accounts/registration/successfully_registered.html"
    page_title = "Activation"

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name)

class ResetUserView(generic.View, core_views.BaseView):

    success_url = reverse_lazy('home')
    page_title = 'Reset'

    def get(self, request, *args, **kwargs):

        print("TODO: password reset not implemented yet")
        return render(request, self.success_url)

class LogoutUserView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        response = logout(request)
        return redirect(self.success_url)

class LoginUserView(generic.FormView, core_views.BaseView):

    form_class = forms.LoginUserForm
    page_title = "Login"
    template_name = 'user_accounts/registration/login.html'
    success_url = reverse_lazy('user_accounts:profile')

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active and not user.is_staff and not user.is_superuser:
                    login(request, user)
                    return redirect(self.success_url)
                else:
                    form.errors[""] = " You aren't allowed to log in here"
            else:
                form.errors['password'] = "Wrong email or password"

        return render(request, self.template_name, { 'form': form, })


class UserConfirmView(generic.View, core_views.BaseView):

    success_url = reverse_lazy('successfully_confirmed')
    page_title = 'Confirmation'

    def get(self, request, confirmation_code):
        record = models.Confirmations.objects.get(confirmation_code=confirmation_code)
        record.has_confirmed = True
        record.save()

        return redirect(self.success_url)

class HasActivatedView(generic.View):

    template_name = "user_accounts/registration/successfully_confirmed.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# TODO: We can delete this right? From what I can tell, all it does is redirect to the homepage,
# but we may as well just do that directly, rather than have this in the middle
# class BackHomepageView(generic.View):
#
#     success_url = reverse_lazy('home')
#
#     def get(self, request, *args, **kwargs):
#         return redirect(self.success_url)
