#from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from administradora.views import LandingView, login


class TestPaginaInicio(TestCase):

    def test_landing_template_view(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        response = LandingView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_login_returns_correct_template(self):
        request = HttpRequest()
        response = login(request)
        expected_html = render_to_string('login.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_login_form(self):
        appuser = Client()
        self.username = 'username'
        self.email = 'user@example.com'
        self.password = 'password'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
        userlogin = appuser.login(username=self.username, password=self.password)
        self.assertEqual(userlogin, True)
