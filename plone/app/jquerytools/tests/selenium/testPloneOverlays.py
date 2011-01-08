import time

import transaction
from base import SeleniumTestCase
from plone.app.testing import PLONE_SITE_ID
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES
from plone.app.testing import helpers
from plone.app.testing.interfaces import TEST_USER_ID

# Note the various time.sleep(...) statements. They're necessary to get
# these tests to run reliably. Is selenium running in an async thread that
# may be interrupting a js function (i.e., checking while it's running) and
# thus catches the DOM in an changing state?

class OverlayTestCase(SeleniumTestCase):
        
    def test_login_overlay(self):
        
        sel = self.selenium

        self.open("/")
        
        # test that click on log-in opens overlay
        sel.click("id=personaltools-login")
        self.waitForElement('form#login_form')
        self.waitForElement("div.overlay-ajax form#login_form")
        self.waitForElement("#exposeMask")
        time.sleep(0.5)
        
        # clicking anywhere else should close overlay
        sel.click("id=exposeMask")
        time.sleep(1)
        self.failIf(sel.is_element_present("id=login_form"))

        # reload overlay
        sel.click("id=personaltools-login")
        self.waitForElement("#login-form")
        
        # click on empty form submit and look for error
        # in overlay
        sel.click("submit")
        self.waitForElement("dl.portalMessage.error")
        self.waitForElement("div.overlay-ajax form#login_form")
        time.sleep(0.5)
        self.failUnless(sel.is_text_present("Error"))

        # Now, try a real login
        sel.type("name=__ac_name", TEST_USER_NAME)
        sel.type("name=__ac_password", TEST_USER_PASSWORD)
        sel.click("submit")
        self.wait()
        self.waitForElement("#personaltools-logout")
        time.sleep(0.5)
        # overlay should be gone
        self.failIf(sel.is_element_present("css=div.overlay-ajax form#login_form"))

        self.open("logout")
        time.sleep(0.5)

    def test_delete_confirm(self):
        # create a test target
        portal = self.layer['portal']
        helpers.setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Folder', 'f1')
        transaction.commit()

        sel = self.selenium
        self.open("/")

        # log in
        sel.click("id=personaltools-login")
        self.waitForElement("#login-form")
        time.sleep(0.5)
        sel.type("name=__ac_name", TEST_USER_NAME)
        sel.type("name=__ac_password", TEST_USER_PASSWORD)
        sel.click("submit")
        self.wait()
        self.waitForElement("#personaltools-logout")
        time.sleep(0.5)

        sel.click("link=f1")
        self.wait()
        
        sel.click("id=delete")
        self.waitForElement("div.overlay-ajax form#delete_confirmation")
        self.waitForElement("#exposeMask")
        self.waitForElement("div.overlay-ajax form#delete_confirmation form.button.Cancel")
        sel.click("form.button.Cancel")
                
        sel.click("id=delete")
        self.waitForElement("div.overlay-ajax form#delete_confirmation form.button.Cancel")
        sel.click("//input[@value='Delete']")

        self.wait()
        time.sleep(0.5)
        
        self.failUnless(sel.get_location().rstrip('/').split('/')[-1] == PLONE_SITE_ID)

        self.failIf(sel.is_element_present("id=portaltab-f1"))
        
        self.open("logout")
        time.sleep(0.5)
