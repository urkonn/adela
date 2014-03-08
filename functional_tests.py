from selenium.webdriver.firefox.webdriver import WebDriver as fdriver
from selenium.webdriver.common.keys import Keys
import unittest


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adela.settings")
from django.test import LiveServerTestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from administradora.views import ProfileView


class SessionTests(LiveServerTestCase):
    def mark_as_pending(self):
        self.assertEqual(1, 0, "pending")

    def setUp(cls):
        cls.selenium = fdriver()
        cls.selenium.implicitly_wait(3)
        super(SessionTests, cls).setUp()
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username='someuser',
                                            email='someuser@example.com', password='somepassword')

    def tearDown(cls):
        cls.selenium.quit()

    #Como anonimo cuando:
    def test_loggedout_user_cannot_see_other_sections_than_home(self):
        #entro a un path, me regresa al landing con un mensaje de error
        self.selenium.get('http://127.0.0.1:8000/restricted')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('404', body.text)

    def test_loggedout_user_can_see_landing_page(self):
        #entro a root, veo el landing
        self.selenium.get('http://127.0.0.1:8000')
        self.assertIn('ADELA', self.selenium.title)

    def test_loggedout_user_see_login_link(self):
        #estoy en landing, veo liga al login
        self.selenium.get('http://127.0.0.1:8000')
        self.selenium.find_element_by_link_text('Login')

    def test_loggedout_user_click_login_link_and_is_redirected_to_login_form(self):
        #hago click en login, veo una forma
        self.selenium.get('http://127.0.0.1:8000')
        self.selenium.find_element_by_link_text('Login').click
        self.selenium.get('http://127.0.0.1:8000/login')
        self.selenium.find_element_by_id('loginForm')

    def test_loggedout_user_fills_login_form_with_invalid_credentials(self):
        #lleno la forma con una cuenta no valida, veo un error
        self.selenium.get('http://127.0.0.1:8000/login')
        loginuserform = self.selenium.find_element_by_name('username')
        loginuserform.send_keys('wronguser')
        loginpasswdform = self.selenium.find_element_by_name('password')
        loginpasswdform.send_keys('wrongpassword')
        loginsubmitform = self.selenium.find_element_by_name('continue')
        loginsubmitform.send_keys(Keys.ENTER)

    def test_loggedout_user_fills_login_form_with_valid_credentials(self):
        #lleno la forma con una cuenta valida me dirigen al home de mi cuenta y veo un msg de exito
        request = self.factory.get('/login')
        request.user = self.user
        self.selenium.get('http://127.0.0.1:8000/login')
        self.selenium.find_element_by_name('username').send_keys('someuser')
        self.selenium.find_element_by_name('password').send_keys('somepassword')
        self.selenium.find_element_by_name('continue').send_keys(Keys.ENTER)
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('profile', body.text)

    #Como usuario cuando:
    def test_loggedin_user_see_user_homepage(self):
        #entro a root debo ver el home de mi cuenta
        request = self.factory.get('/home')
        request.user = self.user
        response = ProfileView
        self.assertTemplateUsed(response, 'home.html')

    def test_loggedin_user_see_her_name(self):
        #entro a root, veo mi nombre
        request = self.factory.get('/home')
        request.user = self.user
        response = ProfileView(request)
        self.selenium.get('%s%s' % (self.live_server_url, '/home'))
        self.assertIn('profile', response.content)

    def test_loggedin_user_see_logout_link(self):
        #entro a root, veo liga para logout
        request = self.factory.get('/home')
        request.user = self.user
        response = ProfileView(request)
        self.selenium.get('%s%s' % (self.live_server_url, '/home'))
        self.assertIn('logout', response.content)

    def test_loggedin_user_gets_404_outside_user_homepage(self):
        #entro a otro path debo ver 404
        request = self.factory.get('/home')
        request.user = self.user
        self.selenium.get('http://127.0.0.1:8000/notfound')
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('404', body.text)

    def test_loggedin_user_logout(self):
        #hago click en logout me dirigen al landing y veo un mensaje de exito.
        self.test_loggedin_user_see_logout_link
        self.selenium.find_element_by_link_text('Logout').click
        self.selenium.find_element_by_id('loginForm')


if __name__ == '__main__':
    unittest.main()
