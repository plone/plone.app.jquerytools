import time
import transaction
import unittest2 as unittest

from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing.selenium_layers import open, click, type
from plone.app.testing import PLONE_SITE_ID
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES
from plone.app.testing import helpers
from plone.app.testing.interfaces import TEST_USER_ID

# Note the various time.sleep(...) statements. They're necessary to get
# these tests to run reliably. Is selenium running in an async thread that
# may be interrupting a js function (i.e., checking while it's running) and
# thus catches the DOM in an changing state?

class OverlayTestCase(unittest.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING
       
    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.driver.implicitly_wait(5)

    def test_login_overlay(self):
        
        open(self.driver, self.portal.absolute_url())
        
        # test that click on log-in opens overlay
        click(self.driver, '#personaltools-login')
	time.sleep(0.5) # sleep necessary after clicks
        self.driver.find_element_by_css_selector('form#login_form')
        self.driver.find_element_by_css_selector('div.overlay-ajax form#login_form')
        self.driver.find_element_by_css_selector('#exposeMask')
        
        # clicking anywhere else should close overlay
        click(self.driver, '#exposeMask')
        time.sleep(0.5)
        self.failIf("login_form" in self.driver.get_page_source())

        # reload overlay
        time.sleep(1)
        click(self.driver, '#personaltools-login')
	time.sleep(0.5)
        self.driver.find_element_by_css_selector("#login-form")
        
        # click on empty form submit and look for error
        # in overlay
        self.driver.find_element_by_name("submit").click()
	time.sleep(0.5)
        self.driver.find_element_by_css_selector("dl.portalMessage.error")
        self.driver.find_element_by_css_selector("div.overlay-ajax form#login_form")
        time.sleep(0.5)
        self.assertTrue("Error" in self.driver.get_page_source()) #portalMessage error

        # Now, try a real login
        type(self.driver, "__ac_name", TEST_USER_NAME)
        type(self.driver, "__ac_password", TEST_USER_PASSWORD)
        # Instead of ...
        #     sel.click("submit")
        # find the element and then click, as in ...
        click(self.driver, "submit")
        time.sleep(5)
        self.driver.find_element_by_id("personaltools-logout")
        time.sleep(0.5)
        # overlay should be gone
#?        self.failIf(sel.is_element_present("css=div.overlay-ajax form#login_form"))
#?        self.failIf(sel.find_element_by_css_selector("div.overlay-ajax form#login_form"))
        self.failIf("login_form" in self.driver.get_page_source())

        click(self.driver, '#user-name')
        time.sleep(0.5)
        click(self.driver, 'link=Log out')
        time.sleep(5)

    def test_delete_confirm(self):
        # create a test target
        helpers.setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'f1')
        transaction.commit()

        open(self.driver, self.portal.absolute_url())

        # log in
        click(self.driver, '#personaltools-login')
        time.sleep(0.2)
        self.driver.find_element_by_css_selector("#login-form")
        time.sleep(0.5)
        type(self.driver, "__ac_name", TEST_USER_NAME)
        type(self.driver, "__ac_password", TEST_USER_PASSWORD)
        click(self.driver, "submit")
        time.sleep(10)
        self.driver.find_element_by_css_selector("#personaltools-logout")
        time.sleep(0.5)

        click(self.driver, "link=f1")
        time.sleep(5)

        # Note the following three examples fail to properly test the
        # content menu Actions drop down
        #     sel.find_element_by_id("plone-contentmenu-actions").click()
        #     sel.find_element_by_css_selector("dt.actionMenuHeader").click()
        #     sel.find_element_by_css_selector("dl#plone-contentmenu-actions.actionMenu").click()
        # instead we find all the drop down menus and ...
        contentActionMenus = self.driver.find_elements_by_class_name("arrowDownAlternative")
        # ... click on the Actions menu
        contentActionMenus[-1].click()
        time.sleep(2)
        click(self.driver, '#delete')
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.overlay-ajax form#delete_confirmation")
        self.driver.find_element_by_css_selector("#exposeMask")
        click(self.driver, "form.button.Cancel")
        time.sleep(2)

        # Alternatively we can search on the partial link text.
        # Note you have to use the partial text in this case as
        # the full link text includes the <span> element
        click(self.driver, "link=Actions")
        time.sleep(0.5)
        click(self.driver, '#delete')
        time.sleep(2)
        # Instead of ...
        #     sel.click("//input[@value='Delete']")
        # use ...
        self.driver.find_element_by_css_selector("input[value='Delete']").click()

        time.sleep(5)

        # Instead of ...
        #  sel.get_location()
        # use ...
        self.failUnless(self.driver.current_url.rstrip('/').split('/')[-1] == PLONE_SITE_ID)

        self.failIf("portaltab-f1" in self.driver.get_page_source())
        
        click(self.driver, '#user-name')
        time.sleep(0.5)
        click(self.driver, 'link=Log out')
        time.sleep(5)

