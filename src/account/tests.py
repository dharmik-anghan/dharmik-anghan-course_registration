from rest_framework import status
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase, force_authenticate

from account.models import User


class AccountTests(APITestCase, URLPatternsTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            first_name="test",
            last_name="test",
            password="testpassword",
            tc=True,
        )
        self.user.save()

    urlpatterns = [
        path("api/user/", include("account.urls")),
    ]

    def test_register_account(self):
        """
        Ensure we can create a new account object.
        """
        data = {
            "email": "dharmikanghan02@gmail.com",
            "first_name": "dharmik",
            "last_name": "anghan",
            "password": 1234,
            "confirm_password": 1234,
            "tc": True,
        }
        url = reverse("register")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_login_account_success(self):
        """
        Ensure we can create a new account object.
        """
        data = {"email": "test@example.com", "password": "testpassword"}
        url = reverse("login")  # Assuming your login endpoint is named 'login'
        response = self.client.post(url, data=data, format="json")

        # Check response
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Assuming successful login returns 200 OK
        self.assertIn("token", response.data)

    def test_login_account_error(self):
        """
        Ensure we can create a new account object.
        """
        data = {"email": "est@example.com", "password": "testpassword"}
        url = reverse("login")  # Assuming your login endpoint is named 'login'
        response = self.client.post(url, data=data, format="json")

        # Check response
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )  # Assuming successful login returns 200 OK
        self.assertIn("errors", response.data)

    def test_profile_view_success(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("profile")  # Assuming your login endpoint is named 'login'
        response = self.client.get(url)

        # Check response
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )  # Assuming successful login returns 200 OK
        self.assertIn("errors", response.data)
