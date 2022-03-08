from django.test import TestCase
from django.contrib.auth.models import User

import json

from rest_framework.test import APIClient
from rest_framework import status



class ActivitytestCase(TestCase):
    def setUp(self):
        user = User(
            email="edmon.af@gmail.com",
            first_name="Edmundo",
            last_name="Andrade",
            username="eandrade",
        )
        user.set_password("1234567890***")
        user.save()


    def test_login(self):
        client = APIClient()

        response = client.post(
            "/api/v1/auth/", {
                "username": "eandrade",
                "password": "1234567890***"
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn("token", result)

    def test_login_w_error(self):
        client = APIClient()

        response = client.post(
            "/api/v1/auth/", {
                "username": "eandrade",
                "password": "1234567890"
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        result = json.loads(response.content)
        self.assertIn("non_field_errors", result)






