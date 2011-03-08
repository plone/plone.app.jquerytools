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

#        self.open("@@p.a.jqt.testPage/", look_for="id=taform")
        self.open(portal.absolute_url()+"/p.a.jqt.testPage")
        time.sleep(2)

#        sel.click("taform")
        sel.find_element_by_id("taform").click()
#?        self.waitForElement("div.overlay-ajax form")
        time.sleep(2)
# ToDo        self.failUnless(sel.is_text_present("Test Form"))
# ToDo        self.failIf(sel.is_text_present("exact:Should not show"))        
# ToDo        self.failUnless(sel.is_text_present("exact:ajax_load:"))

#        sel.type("Password", "xxx")
        sel.find_element_by_name("Password").send_keys("xxx")
#        sel.click("//input[@name='Check' and @value='3']")
        sel.find_element_by_css_selector("input[name='Check'][value='3']").click()
#        sel.click("//input[@name='Radio' and @value='3']")
        sel.find_element_by_css_selector("input[name='Radio'][value='3']").click()
#        sel.click("submitButton")
        sel.find_element_by_css_selector("input[name='submitButton'][value='Submit1']").click()
        time.sleep(3)

# ToDo        self.failUnless(sel.is_text_present("exact:ajax_load:"))
# ToDo        self.failUnless(sel.is_text_present("exact:Multiple:one"))
# ToDo        self.failUnless(sel.is_text_present("exact:Name:MyName1"))
# ToDo        self.failUnless(sel.is_text_present("exact:Single2:A"))
# ToDo        self.failUnless(sel.is_text_present("exact:Single:one"))
# ToDo        self.failUnless(sel.is_text_present("exact:Radio:3"))
# ToDo        self.failUnless(sel.is_text_present("exact:Text:This is Form1"))
# ToDo        self.failUnless(sel.is_text_present("exact:submitButton:Submit1"))
# ToDo        self.failUnless(sel.is_text_present("exact:Hidden:hiddenValue"))
# ToDo        self.failUnless(sel.is_text_present("exact:Password:xxx"))
# ToDo        self.failUnless(sel.is_text_present("exact:Check:3"))
        
        # Make sure we can handle other submit methods, and that the
        # value of the submit button is in the request
        sel.find_element_by_css_selector("input[name='submitButton'][value='Submit2']").click()
        time.sleep(3)
# ToDo        self.failUnless(sel.is_text_present("exact:submitButton:Submit2"))
#        sel.click("//button[@name='submitButton']")
        sel.find_element_by_css_selector("button[name='submitButton']").click()
        time.sleep(3)
# ToDo        self.failUnless(sel.is_text_present("exact:submitButton:Submit5"))

        # pushing submit6 should close the overlay
#        sel.click("//input[@name='submitButton6']")
        sel.find_element_by_css_selector("input[name='submitButton6']").click()
        time.sleep(3)
# ToDo        self.failIf(sel.is_text_present("Test Form"))
