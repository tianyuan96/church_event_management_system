from .forms import RegisterOrganisationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


class OrganisationProfileView(LoginRequiredMixin, generic.TemplateView):

    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'organisation': request.user})

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

            user = form.save(commit=False)
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            # Auto log the user in
            user = authenticate(username=username, password=password)

            if user is not None: # if the user was successfully authed
                if user.is_active:  # The user has not been banned
                    login(request, user)
                    return redirect(self.success_url)
        return render(request, self.template_name, {'form': form })
