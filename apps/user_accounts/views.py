from .forms import RegisterUserForm, LoginUserForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from . import models
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from apps.events.models import InvolvedEvent, Event
from apps.surveys.forms import FoodPreferencesForm
from apps.surveys.models import FoodPreferences



class UserProfileView(generic.UpdateView):

    template_name = "registration/profile.html"
    form_class = FoodPreferencesForm
    success_url = reverse_lazy('user_profile')
    page_title = "Profile"

    def get_object(self, queryset=None):
        # return self.request.user.foodpreferences
        obj, _ = FoodPreferences.objects.get_or_create(user=self.request.user)
        return obj

    """
        Below are attributes that can be rendered in the template, for example {{ view.title }}
    """
    def title(self):
        return self.page_title

    def events(self):

        # If user is not logged in, then filter() tries to get all the events an AnonymousUser has, and then fails.
        # I don't know why it would do that and not just return an empty list, or None, but whatever
        if not self.request.user.is_authenticated:
            return []

        # we want to get the Events here, not the InvolvedEvents, since we need Event data
        return Event.objects.filter(involvedevent__participant=self.request.user)

class RegisterUserView(generic.View):

    form_class = RegisterUserForm
    title = "Register"
    template_name = 'registration/register.html'
    #success_url = reverse_lazy('user_profile')
    success_url = reverse_lazy('successfully_registered')
    profile_url = reverse_lazy('user_profile')
    # Display the register account page
    def get(self, request, *args, **kwargs):

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'title': self.title})

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

class NeedActivateView(generic.View):

    template_name = "registration/successfully_registered.html"


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ResetUserView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        print("TODO: password reset not implemented yet")
        return render(request, self.success_url)

class LogoutUserView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        response = logout(request)
        return redirect(self.success_url)

class LoginUserView(generic.View):

    form_class = LoginUserForm
    page_title = "Logins"
    template_name = 'registration/login.html'
    success_url = reverse_lazy('user_profile')
    context = {'title': page_title}

    def get(self, request, *args, **kwargs):

        form = self.form_class(None)
        self.context['form'] = form
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(self.success_url)
            else:
                print("Invalid Login, should redirect to error page")

        self.context['form'] = form
        return render(request, self.template_name, self.context)

class BackHomepageView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        print("DKSFJLDKSJFLSK")
        return redirect(self.success_url)

class UserConfirmView(generic.View):
    success_url = reverse_lazy('successfully_confirmed')

    def get(self, request, confirmation_code):
        record = models.Confirmations.objects.get(confirmation_code=confirmation_code)
        record.has_confirmed = True
        record.save()

        return redirect(self.success_url)

class HasActivatedView(generic.View):

    template_name = "registration/successfully_confirmed.html"


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
