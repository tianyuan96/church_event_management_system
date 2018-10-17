from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import io
from contextlib import redirect_stdout
from django.core import management
from django.urls import resolve, reverse
from django.contrib import auth
class UserTest(TestCase):


    def setUp(self):

        self.creds = { 'email': 'b@b.com', 'password': 'password', 'username': 'b@b.com', }
        user = User.objects.create(username=self.creds['username'])
        user.set_password(self.creds['password'])  # store the plaintext password, not the hash
        user.save()
        self.client = Client()

    def test_login(self):

        user = auth.get_user(self.client)

        # Just get the login page
        response = self.client.get(reverse('user_accounts:login'))
        assert(response.status_code == 200)
        assert(user.is_authenticated == False)

        # POST request with no data
        response = self.client.post(reverse('user_accounts:login'))
        assert(response.status_code == 200)
        assert(user.is_authenticated == False)


    def test_user_profile(self):
        # logged out user
        response = self.client.get(reverse('user_accounts:profile'), follow=True)

        self.assertNotIn(str(response.context), 'user')
        self.assertEqual(response.status_code, 404)

        logged_in = self.client.login(username=self.creds['username'], password=self.creds['password'])
        response = self.client.get(reverse('user_accounts:profile'), follow=True)
        self.assertEqual(response.context['user'].username, self.creds['username']) # email would be 'anonymous' if the user is not logged in
        self.assertEqual(response.status_code, 200)

        
