from django.test import TestCase
from django.test import Client
from .forms import *
from django.contrib.auth.models import User
#from .models import Entry, Comment

# Create your tests here.
class EntryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="staff@focuschurch.com.au", email="staff@focuschurch.com.au", password="qaws123ed")

class OrgViewTest(EntryModelTest):
    # Test organisation views
    def test_org_view(self):
        response = self.client.post()
class OrgFormTest(TestCase):
    # Test organisation forms
    def test_invalid_data(self):
        invalid_data = [
        # Error in email, needs @ symbol
        { 'data' : {'organisation' : "Focus Church", 'email' : "staffedu.com.au", 'password1' : "qaws123ed", 'password2' : "qaws123ed"},
        'error' : ('email', [u"Enter a valid email address."]) },
        # Error in email, needs a .
        { 'data' : {'organisation' : "Focus Church", 'email' : "staff@comau", 'password1' : "qaws123ed", 'password2' : "qaws123ed"},
        'error' : ('email', [u"Enter a valid email address."]) },
        # Passwords do not match
        { 'data' : {'organisation' : "Focus Church", 'email' : "staff@edu.com.au", 'password1' : "qaws123ed", 'password2' : "password"},
        'error' : ('password2', [u"The two password fields didn't match."]) },

        ]
        for d in invalid_data:
            form = RegisterOrganisationForm(data=d['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[d['error'][0]], d['error'][1])

    def test_valid_data(self):
        # Test a valid form entry
        form = RegisterOrganisationForm(data={ 'organisation': 'Focus Church',
                                             'email': 'staff@edu.com.au',
                                             'password1': 'fcschch2019',
                                             'password2': 'fcschch2019' })
        self.assertTrue(form.is_valid())
