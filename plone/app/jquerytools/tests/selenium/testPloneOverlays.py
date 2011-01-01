import time

from base import SeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES

class OverlayTestCase(SeleniumTestCase):
        
    def test_login_overlay(self):
        
        self.open("/")
        self.wait()
        sel = self.selenium

        # test that click on log in opens overlay
        sel.click("personaltools-login")
        self.waitForElement('form#login_form')
        self.failUnless(sel.is_element_present("css=div.overlay-ajax form#login_form"))
        
        # clicking anywhere else should close overlay
        sel.click("exposeMask")
        time.sleep(0.5)
        self.failIf(sel.is_element_present("id=login_form"))

        # reload overlay
        sel.click("personaltools-login")
        self.waitForElement("#login-form")
        
        # click on empty form submit and look for error
        # in overlay
        sel.click("submit")
        self.waitForElement("dl.portalMessage.error")
        self.failUnless(sel.is_element_present("css=div.overlay.overlay-ajax form#login_form"))
        self.failUnless(sel.is_text_present("Error"))

        # Now, try a real login
        sel.type("name=__ac_name", TEST_USER_NAME)
        sel.type("name=__ac_password", TEST_USER_PASSWORD)
        sel.click("submit")
        self.wait()
        # overlay should be gone
        self.failIf(sel.is_element_present("css=div.overlay-ajax form#login_form"))
        self.failUnless(sel.is_element_present("id=personaltools-logout"))
        

