import sys
import time

from base import SeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES

class FormTestCase(SeleniumTestCase):
    """Tests form input marshaling for complex forms
    *** Note: These test are currently incomplete. ***
    """
    def test_afancy_form(self):
        """ test basic form functions on a complex form """

        sel = self.selenium
	portal = self.portal

        self.open(portal.absolute_url()+"/p.a.jqt.testPage")
        time.sleep(2)

        sel.find_element_by_id("taform").click()
#?        self.waitForElement("div.overlay-ajax form")
        time.sleep(2)
        # Instead of ...
        #     self.failUnless(sel.is_text_present("Test Form"))
        # use ...
        self.failUnless(self.isTextPresent("Test Form"))
        self.failIf(self.isTextPresent("Should not show"))        
        self.failUnless(self.isTextPresent("ajax_load:"))

        sel.find_element_by_name("Password").send_keys("xxx")
        sel.find_element_by_css_selector("input[name='Check'][value='3']").click()
        sel.find_element_by_css_selector("input[name='Radio'][value='3']").click()
        sel.find_element_by_css_selector("input[name='submitButton'][value='Submit1']").click()
        time.sleep(3)

        self.failUnless(self.isTextPresent("ajax_load:"))
        self.failUnless(self.isTextPresent("Multiple:one"))
        self.failUnless(self.isTextPresent("Name:MyName1"))
        self.failUnless(self.isTextPresent("Single2:A"))
        self.failUnless(self.isTextPresent("Single:one"))
        self.failUnless(self.isTextPresent("Radio:3"))
        self.failUnless(self.isTextPresent("Text:This is Form1"))
        self.failUnless(self.isTextPresent("submitButton:Submit1"))
        self.failUnless(self.isTextPresent("Hidden:hiddenValue"))
        self.failUnless(self.isTextPresent("Password:xxx"))
        self.failUnless(self.isTextPresent("Check:3"))
        
        # Make sure we can handle other submit methods, and that the
        # value of the submit button is in the request
        sel.find_element_by_css_selector("input[name='submitButton'][value='Submit2']").click()
        time.sleep(3)
        self.failUnless(self.isTextPresent("submitButton:Submit2"))
        sel.find_element_by_css_selector("button[name='submitButton']").click()
        time.sleep(3)
        self.failUnless(self.isTextPresent("submitButton:Submit5"))

        # pushing submit6 should close the overlay
        sel.find_element_by_css_selector("input[name='submitButton6']").click()
        time.sleep(3)
        self.failIf(self.isTextPresent("Test Form"))