import sys
import time
import unittest2 as unittest

from plone.app.testing import selenium_layers as layers
from plone.app.testing.selenium_layers import open, click, type
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES

class FormTestCase(unittest.TestCase):
    """Tests form input marshaling for complex forms
    *** Note: These test are currently incomplete. ***
    """
    layer = layers.SELENIUM_PLONE_FUNCTIONAL_TESTING
    
    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

    def test_afancy_form(self):
        """ test basic form functions on a complex form """

        open(self.driver, self.portal.absolute_url()+"/p.a.jqt.testPage")
        time.sleep(2)

        click(self.driver, "#taform")
#?        self.waitForElement("div.overlay-ajax form")
        time.sleep(2)
        self.failUnless("Test Form" in self.driver.get_page_source())
        self.failIf("Should not show" in self.driver.get_page_source())        
        self.failUnless("ajax_load:" in self.driver.get_page_source())

        type(self.driver, "Password", "xxx")
        self.driver.find_element_by_css_selector("input[name='Check'][value='3']").click()
        self.driver.find_element_by_css_selector("input[name='Radio'][value='3']").click()
        self.driver.find_element_by_css_selector("input[name='submitButton'][value='Submit1']").click()
        time.sleep(3)

        self.failUnless("ajax_load:" in self.driver.get_page_source())
        self.failUnless("Multiple:one" in self.driver.get_page_source())
        self.failUnless("Name:MyName1" in self.driver.get_page_source())
        self.failUnless("Single2:A" in self.driver.get_page_source())
        self.failUnless("Single:one" in self.driver.get_page_source())
        self.failUnless("Radio:3" in self.driver.get_page_source())
        self.failUnless("Text:This is Form1" in self.driver.get_page_source())
        self.failUnless("submitButton:Submit1" in self.driver.get_page_source())
        self.failUnless("Hidden:hiddenValue" in self.driver.get_page_source())
        self.failUnless("Password:xxx" in self.driver.get_page_source())
        self.failUnless("Check:3" in self.driver.get_page_source())
        
        # Make sure we can handle other submit methods, and that the
        # value of the submit button is in the request
        self.driver.find_element_by_css_selector("input[name='submitButton'][value='Submit2']").click()
        time.sleep(3)
        self.failUnless("submitButton:Submit2" in self.driver.get_page_source())
        self.driver.find_element_by_css_selector("button[name='submitButton']").click()
        time.sleep(3)
        self.failUnless("submitButton:Submit5" in self.driver.get_page_source())

        # pushing submit6 should close the overlay
        self.driver.find_element_by_css_selector("input[name='submitButton6']").click()
        time.sleep(3)
        self.failIf("Test Form" in self.driver.get_page_source())