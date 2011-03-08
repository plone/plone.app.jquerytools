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
	portal = self.portal

        # Selenium 2.0 uses implicit waits for each find_element_by... calls
	self.setWaitTimeout(5)

        self.open(portal.absolute_url())
        
        # test that click on log-in opens overlay
        sel.find_element_by_id('personaltools-login').click()
	time.sleep(0.5) # sleep necessary after clicks
        sel.find_element_by_css_selector('form#login_form')
        sel.find_element_by_css_selector('div.overlay-ajax form#login_form')
        sel.find_element_by_css_selector('#exposeMask')
#	time.sleep(0.5)
        
        # clicking anywhere else should close overlay
        sel.find_element_by_id('exposeMask').click()
        time.sleep(0.5)
        # Instead of ...
        #     self.failIf(sel.is_element_present("id=login_form"))
        # use ...
        self.failIf(self.isElementPresent("login_form"))

        # reload overlay
        time.sleep(1)
        sel.find_element_by_id('personaltools-login').click()
	time.sleep(0.5)
        sel.find_element_by_css_selector("#login-form")
        
        # click on empty form submit and look for error
        # in overlay
        sel.find_element_by_name("submit").click()
	time.sleep(0.5)
        sel.find_element_by_css_selector("dl.portalMessage.error")
        sel.find_element_by_css_selector("div.overlay-ajax form#login_form")
        time.sleep(0.5)
        #self.failUnless(sel.is_text_present("Error")) #portalMessage error

        # Now, try a real login
        sel.find_element_by_name("__ac_name").send_keys(TEST_USER_NAME)
        sel.find_element_by_name("__ac_password").send_keys(TEST_USER_PASSWORD)
        # Instead of ...
        #     sel.click("submit")
        # find the element and then click, as in ...
        sel.find_element_by_name("submit").click()
        time.sleep(5)
        sel.find_element_by_id("personaltools-logout")
        time.sleep(0.5)
        # overlay should be gone
#        self.failIf(sel.is_element_present("css=div.overlay-ajax form#login_form"))
#        self.failIf(sel.find_element_by_css_selector("div.overlay-ajax form#login_form"))
        self.failIf(self.isElementPresent("login_form"))

        sel.find_element_by_id('user-name').click()
        time.sleep(0.5)
        sel.find_element_by_link_text('Log out').click()
        time.sleep(5)

    def test_delete_confirm(self):
        # create a test target
        portal = self.portal
        helpers.setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Folder', 'f1')
        transaction.commit()

        sel = self.selenium

	self.setWaitTimeout(20)
                
        self.open(portal.absolute_url())

        # log in
        sel.find_element_by_id('personaltools-login').click()
        time.sleep(0.2)
        sel.find_element_by_css_selector("#login-form")
        time.sleep(0.5)
        sel.find_element_by_name("__ac_name").send_keys(TEST_USER_NAME)
        sel.find_element_by_name("__ac_password").send_keys(TEST_USER_PASSWORD)
        sel.find_element_by_name("submit").click()
        time.sleep(10)
        sel.find_element_by_css_selector("#personaltools-logout")
        time.sleep(0.5)

        sel.find_element_by_link_text("f1").click()
        time.sleep(5)

        # Note the following three examples fail to properly test the
        # content menu Actions drop down
        #     sel.find_element_by_id("plone-contentmenu-actions").click()
        #     sel.find_element_by_css_selector("dt.actionMenuHeader").click()
        #     sel.find_element_by_css_selector("dl#plone-contentmenu-actions.actionMenu").click()
        # instead we find all the drop down menus and ...
        contentActionMenus = sel.find_elements_by_class_name("arrowDownAlternative")
        # ... click on the Actions menu
        contentActionMenus[-1].click()
        time.sleep(2)
        sel.find_element_by_id('delete').click()
        time.sleep(2)
        sel.find_element_by_css_selector("div.overlay-ajax form#delete_confirmation")
        sel.find_element_by_css_selector("#exposeMask")
        sel.find_element_by_name("form.button.Cancel").click()
        time.sleep(2)

        # Alternatively we can search on the partial link text.
        # Note you have to use the partial text in this case as
        # the full link text includes the <span> element
        sel.find_element_by_partial_link_text("Actions").click()
        time.sleep(0.5)
        sel.find_element_by_id('delete').click()
        time.sleep(2)
#        sel.find_element_by_css_selector("div.formControls form#delete_confirmation form.button.Cancel")
        # Instead of ...
#       #     sel.click("//input[@value='Delete']")
        # use ...
        sel.find_element_by_css_selector("input[value='Delete']").click()

        time.sleep(5)

        # Instead of ...
        #  sel.get_location()
        # use ...
        self.failUnless(sel.current_url.rstrip('/').split('/')[-1] == PLONE_SITE_ID)

        self.failIf(self.isElementPresent("portaltab-f1"))
        
        sel.find_element_by_id('user-name').click()
        time.sleep(0.5)
        sel.find_element_by_link_text('Log out').click()
        time.sleep(5)

