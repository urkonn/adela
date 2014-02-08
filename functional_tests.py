from selenium import webdriver
import unittest


class AppUserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    #Como anonimo cuando:
    def test_loggedout_user_cannot_see_other_sections_than_home(self):
        #entro a un path, me regresa al landing con un mensaje de error
        pass

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
        pass

    def test_loggedout_user_fills_login_form_with_valid_credentials(self):
        #lleno la forma con una cuenta valida me dirigen al home de mi cuenta y veo un msg de exito
        pass

    #Como usuario cuando:
    def test_loggedin_user_see_user_homepage(self):
        #entro a root debo ver el home de mi cuenta
        pass

    def test_loggedin_user_see_her_name(self):
        #entro a root, veo mi nombre
        pass

    def test_loggedin_user_see_logout_link(self):
        #entro a root, veo liga para logout
        pass

    def test_loggedin_user_gets_404_outside_user_homepage(self):
        #entro a otro path debo ver 404
        pass

    def test_loggedin_user_logout(self):
        #hago click en logout me dirigen al landing y veo un mensaje de exito.
        pass

if __name__ == '__main__':
    unittest.main(warnings='ignore')
