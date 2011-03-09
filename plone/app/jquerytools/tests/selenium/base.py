import string
import time
import selenium
import transaction
import unittest2 as unittest

from plone.app.testing import selenium_layers as layers
from selenium.webdriver.common.exceptions import NoSuchElementException


class SeleniumTestCase(unittest.TestCase):
    layer = layers.SELENIUM_PLONE_FUNCTIONAL_TESTING
    
    def setUp(self):
        self.selenium = self.layer['selenium']
        self.portal   = self.layer['portal']

    def open(self, url):
        # ensure we have a clean starting point
        transaction.commit()
        self.selenium.get(url)

    def setWaitTimeout(self, timeout=30):
        """
        """
        self.selenium.implicitly_wait(timeout)

    def isElementPresent(self, element):
        """
        ToDo:
          - add identifyBy parameter to allow for using other
            find_element_by... functions
        """
        try:
            self.selenium.find_element_by_id(element)
        except NoSuchElementException:
            return False

        return True

    def isTextPresent(self, text):
        """
        """
        if string.find(self.selenium.get_page_source(),text) == -1:
            return False
        else:
            return True

#    def wait(self, timeout="30000"):
#        self.selenium.wait_for_page_to_load(timeout)
#        
#    def waitForElement(self, selector, timeout="30000"):
#        """Continue checking for the element matching the provided CSS
#        selector."""
#        self.selenium.wait_for_condition("""css="%s" """ % selector, timeout)