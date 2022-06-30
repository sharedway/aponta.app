from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import hashlib
from accounts.serializers import AccountSerializer
from accounts.views import ProfileViewSet
from rest_framework.renderers import (
    AdminRenderer,
    BaseRenderer,
    BrowsableAPIRenderer,
    DocumentationRenderer,
    HTMLFormRenderer,
    JSONRenderer,
    SchemaJSRenderer,
    StaticHTMLRenderer,
)

User = get_user_model()


class ProfileViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "demo2020"
        cls.password = "demo@2020"
        cls.first_name = "First Name"
        cls.email = "demo2020@sharedway.app"

    def setUp(self):
        self.user = User.objects.create_user(
            email=self.email,
            first_name=self.first_name,
            last_name="Last Name",
            username=self.username,
            password=self.password,
        )
        self.token = Token.objects.get(user=self.user)
        self.badToken = "sdsds9sidsaaadasdasd6trgasjjsd"

    def test_api_view_set(self):
        headers = {"Authorization": "Bearer {token}".format(token=self.token.key)}
        api_request = APIRequestFactory().get(
            "/rest-api/accounts/profile/",
            format="json",
            **headers,
        )
        api_request.user = self.user
        detail_view = ProfileViewSet.as_view({"get": "retrieve"})
        response = detail_view(api_request, pk=self.user.id)
        renderer = JSONRenderer()
        content = renderer.render(response.data, "application/json; indent=2")
        self.assertIsNotNone(content)
        self.assertEqual(response.status_code, 200)
