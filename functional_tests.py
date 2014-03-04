from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import mock
import datetime

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adela.settings")
from django.conf import settings
from django.utils.importlib import import_module
from django.utils import timezone
from django.test import TestCase
from django.test.client import Client
from django.contrib.sessions.models import Session
from administradora.views import ProfileView


class AppUserTest(TestCase):
    def mark_as_pending(self):
        self.assertEqual(1, 0, "pending")

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def create_session(self):
        appuser = Client()
        appuser.login(username='username', password='password')
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        s = Session(expire_date=timezone.now() + datetime.timedelta(days=1), session_key=store.session_key)
        s.save()

    #Como anonimo cuando:
    def test_loggedout_user_cannot_see_other_sections_than_home(self):
        #entro a un path, me regresa al landing con un mensaje de error
        self.browser.get('http://127.0.0.1:8000/restricted')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('404', body.text)

    def test_loggedout_user_can_see_landing_page(self):
        #entro a root, veo el landing
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('ADELA', self.browser.title)

    def test_loggedout_user_see_login_link(self):
        #estoy en landing, veo liga al login
        self.browser.get('http://127.0.0.1:8000')
        self.browser.find_element_by_link_text('Login')

    def test_loggedout_user_click_login_link_and_is_redirected_to_login_form(self):
        #hago click en login, veo una forma
        self.browser.get('http://127.0.0.1:8000')
        self.browser.find_element_by_link_text('Login').click
        self.browser.get('http://127.0.0.1:8000/login')
        self.browser.find_element_by_id('loginForm')

    def test_loggedout_user_fills_login_form_with_invalid_credentials(self):
        #lleno la forma con una cuenta no valida, veo un error
        self.browser.get('http://127.0.0.1:8000/login')
        loginuserform = self.browser.find_element_by_name('username')
        loginuserform.send_keys('wronguser')
        loginpasswdform = self.browser.find_element_by_name('password')
        loginpasswdform.send_keys('wrongpassword')
        loginsubmitform = self.browser.find_element_by_name('continue')
        loginsubmitform.send_keys(Keys.ENTER)

    def test_loggedout_user_fills_login_form_with_valid_credentials(self):
        #lleno la forma con una cuenta valida me dirigen al home de mi cuenta y veo un msg de exito
        self.browser.get('http://127.0.0.1:8000/login')
        loginuserform = self.browser.find_element_by_name('username')
        loginuserform.send_keys('username')
        loginpasswdform = self.browser.find_element_by_name('password')
        loginpasswdform.send_keys('password')
        loginsubmitform = self.browser.find_element_by_name('continue')
        loginsubmitform.send_keys(Keys.ENTER)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('profile', body.text)

    #Como usuario cuando:
    def test_loggedin_user_see_user_homepage(self):
        #entro a root debo ver el home de mi cuenta
        self.session = {"usersession": "123456"}
        with mock.patch('django.contrib.auth.models.User') as user_mock:
            user_mock.objects = mock.Mock()
            config = {'get_return_value': mock.Mock()}
            user_mock.objects.configure_mock(**config)
            resp = ProfileView()
            self.session = {}
            expected_template = 'home.html'
            self.assertEquals(resp.template_name, expected_template)

    def test_loggedin_user_see_her_name(self):
        #entro a root, veo mi nombre
        self.create_session()
        self.browser.get('http://127.0.0.1:8000/home')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('profile', body.text)

    def test_loggedin_user_see_logout_link(self):
        #entro a root, veo liga para logout
        self.mark_as_pending()

    def test_loggedin_user_gets_404_outside_user_homepage(self):
        #entro a otro path debo ver 404
        self.mark_as_pending()

    def test_loggedin_user_logout(self):
        #hago click en logout me dirigen al landing y veo un mensaje de exito.
        self.mark_as_pending()

if __name__ == '__main__':
    unittest.main()
