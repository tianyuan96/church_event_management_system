from django.test import TestCase
from django.contrib.auth.models import User

class UserTest(TestCase):

    def setUp(self):
        User.objects.create(email='random@gmail.com', password='auise1234', username='random@gmail.com')
        #User.objects.create(email='random1@gmail.com', password='auise1234', username='random@gmail.com')


    def testWorkingUser(self):
        user1 = User.objects.get(username='random@gmail.com')
        # Test that the email becomes our username
        self.assertEqual(user1.email, user1.username)
        # Test that the password is greater than 8 characters
        self.assertTrue(len(user1.password)>8)
        #self.assertIs(user1.password, int(user1.password))
        self.assertIn('@', user1.email)
        # Testing that the password is all numeric
        try:
            int(user1.password)
            raise AssertionError
        except ValueError:
        # If it is not we can continue
            pass
