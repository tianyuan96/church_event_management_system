from .forms import RegisterUserForm, LoginUserForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileView(generic.TemplateView):

    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user': request.user, 'title': request.user.email})

class RegisterUserView(generic.View):

    form_class = RegisterUserForm
    title = "Register"
    template_name = 'registration/register.html'
    success_url = reverse_lazy('user_profile')

    # Display the register account page
    def get(self, request, *args, **kwargs):

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'title': self.title})

    # Get the data from the registration form and register the user
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            # Auto log the user in
            user = authenticate(email=email, password=password)

            if user is not None: # if the user was successfully authed
                if user.is_active:  # The user has not been banned
                    login(request, user)
                    return redirect(self.success_url)
        return render(request, self.template_name, {'form': form })

class ResetUserView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        print("TODO: password reset not implemented yet")
        return render(request, self.success_url)

class LogoutUserView(generic.View):

    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        print("DKSFJLDKSJFLSK")
        response = logout(request)
        return redirect(self.success_url)

class LoginUserView(generic.View):

    form_class = LoginUserForm
    page_title = "Logins"
    template_name = 'registration/login.html'
    success_url = reverse_lazy('user_profile')

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
