import time

from base import SeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES

class OverlayTestCase(SeleniumTestCase):
        
    def test_login_overlay(self):
        
        self.open("/")
        self.wait()
        sel = self.selenium

        sel.click("personaltools-login")
        self.waitForElement('form#login_form')
        self.failUnless(sel.is_element_present("css=div.overlay.overlay-ajax form#login_form"))
        sel.click("exposeMask")
        time.sleep(0.5)
        self.failIf(sel.is_element_present("id=login_form"))
      
        sel.click("personaltools-login")
        self.waitForElement('form#login_form')
        sel.type("name=__ac_name", TEST_USER_NAME)
        sel.type("name=__ac_password", TEST_USER_PASSWORD)
        sel.click("submit")
        self.wait()
        self.failUnless(sel.is_text_present("Log out"))

