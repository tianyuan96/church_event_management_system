from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import io
from contextlib import redirect_stdout
from django.core import management
from django.urls import resolve

class EntryModelTest(TestCase):

    def setUp(self):
        pass

    def test_all_urls(self):

        # Get all resolvable routes
        f = io.StringIO()
        with redirect_stdout(f):
            management.call_command('show_urls')
        urls = f.getvalue()

        # Iterate over the urls and test whether they return the correct response code
        client = Client()
        for line in urls.split('\n'):
            # line is tab separated in the form: url, view_class, and an optional view_name
            vals = line.strip().split('\t')
            url = vals[0]
            try:
                response = client.get(url)
                print(response.status_code)
            except Exception as e:
                print('FAILED ON:', url)
                print('ERROR WAS:', type(e).__name__)
                assert False

        assert True
