"""Contains test for web pages with selenium"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

# Web Pages Testing with selenium

class ClientSideTesting(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_invalid_register_inputs(self):
        """Tests client side validation of register form"""
        self.selenium.get(f"{self.live_server_url}/register")

        # submit without any input
        register_form = self.selenium.find_element_by_id('register-form')
        register_form.submit()

        # is invalid feedback shown?
        invalid_feedback = self.selenium.find_elements_by_class_name('invalid-feedback');
        for feedback in invalid_feedback:
            self.assertTrue(feedback.is_displayed())

    def test_invalid_login_inputs(self):
        """Tests client side validation of login form"""
        self.selenium.get(f"{self.live_server_url}/login")

        # submit login form without any input
        login_form = self.selenium.find_element_by_id('login-form')
        login_form.submit()

        # is invalid feedback shown?
        invalid_feedback = self.selenium.find_elements_by_class_name('invalid-feedback')
        for feedback in invalid_feedback:
            self.assertTrue(feedback.is_displayed())