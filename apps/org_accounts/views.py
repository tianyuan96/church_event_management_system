from .forms import RegisterOrganisationForm, LoginOrganisationForm
from .models import OrganisationDetails
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.events.models import Event

from apps.events.models import Event

class OrganisationProfileView(LoginRequiredMixin, generic.ListView):

    template_name = "registration/org_profile.html"
    context_object_name = "events"
    model = Event


# Create your views here.
class RegisterOrganisationView(generic.View):

    form_class = RegisterOrganisationForm
    title = "Register Organisation"
    template_name = 'registration/org_register.html'
    success_url = reverse_lazy('org_profile')

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
            user.is_staff = True # grant staff privilege
            user.save()

            # Store the orgs other details as well
            org = OrganisationDetails(name=form.cleaned_data['organisation'], user=user)
            org.save()

            # Auto log the user in
            user = authenticate(username=username, password=password)

            if user is not None: # if the user was successfully authed
                if user.is_active:  # The user has not been banned
                    login(request, user)
                    print("SUCCESSFULLY CREATED ORGANISATION")
                    return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, })



class LoginOrganisationView(generic.View):

    form_class = LoginOrganisationForm
    page_title = "Logins"
    template_name = 'registration/login.html'
    success_url = reverse_lazy('org_profile')

    ctx = {'title': page_title}
    def get(self, request, *args, **kwargs):

        form = self.form_class(None)
        self.ctx['form'] = form
        return render(request, self.template_name, self.ctx)


    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(self.success_url)

        self.ctx['form'] = form
        return render(request, self.template_name, self.ctx)

class LogoutOrganisationView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        response = logout(request)
        return redirect(self.success_url)
