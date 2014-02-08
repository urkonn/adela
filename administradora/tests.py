from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from administradora.views import landing, login


class TestPaginaInicio(TestCase):
    def test_url_resolves_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, landing)

    def test_home_returns_correct_template(self):
        request = HttpRequest()
        response = landing(request)
        expected_html = render_to_string('landing.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_url_resolves_login_page_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func, login)

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
