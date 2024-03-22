from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
from rest_framework_simplejwt.tokens import AccessToken


class UserRegistrationTestCase(TestCase):
    def test_user_registration_success(self):
        client = APIClient()
        data = {
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": 123456,
            "confirm_password": 123456,
            "term": True,
        }
        response = client.post("/api/user/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User Registration Success")
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["status_code"], 201)

    def test_user_registration_error(self):
        client = APIClient()
        data = {
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": 123456,
            "confirm_password": 123456,
        }
        response = client.post("/api/user/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword",
            first_name="first_name",
            last_name="last_name",
            confirm_password="testpassword",
            term=True,
        )

    def test_user_login_success(self):
        client = APIClient()
        data = {"email": "testuser@test.com", "password": "testpassword"}
        response = client.post("/api/user/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["message"], "User Login Success")

    def test_user_login_error(self):
        client = APIClient()
        data = {"email": "testuser@test.com", "password": "testpasssword"}
        response = client.post("/api/user/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword",
            first_name="first_name",
            last_name="last_name",
            confirm_password="testpassword",
            term=True,
        )
        self.token = AccessToken.for_user(self.user)

    def test_user_profile_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/user/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_authenticated(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = client.get("/api/user/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "User Found Success")
