from .forms import RegisterAccountForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, generic.TemplateView):

    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user': request.user})

class RegisterAccountView(generic.View):

    form_class = RegisterAccountForm
    success_url = reverse_lazy('home')
    title = "Register"
    template_name = 'registration/register.html'

    # Display the register account page
    def get(self, request, *args, **kwargs):

        form = self.form_class(None)
        print("GET REQUSET RECEIVED")
        return render(request, self.template_name, {'form': form, 'title': self.title})

    # Get the data from the registration form and register the user
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
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
