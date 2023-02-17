from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class MovieViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/movies/"

        cls.super_user = User.objects.create_superuser(
            username="super1",
            password="1234",
            email="superuser@email.com",
            first_name="user",
            last_name="user",
            is_employee=True,
        )

        super_user_token = RefreshToken.for_user(cls.super_user)

        cls.normal_user = User.objects.create_user(
            username="mormal1",
            password="1234",
            email="normaluser@email.com",
            first_name="user",
            last_name="user",
            is_employee=False,
        )

        normal_user_token = RefreshToken.for_user(cls.normal_user)

    def test_movie_creation_without_token(self):
        movie_data = {
            "title": "titulo",
            "duration": "110min",
        }

        response = self.client.post(self.BASE_URL, data=movie_data, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code

        message = (
            f"Verrifque se o status code retornado do POST"
            + f"em {self.BASE_URL} sem token de usuario válido é {expected_status_code}"
        )

        self.assertEqual(expected_status_code, resulted_status_code, message)
