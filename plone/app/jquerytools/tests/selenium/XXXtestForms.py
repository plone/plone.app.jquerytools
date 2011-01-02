import time

from base import SeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES

class FormTestCase(SeleniumTestCase):
        
    def test_fancy_form(self):
        """ test basic form functions on a complex form """
        
        sel = self.selenium

        sel.open("/plone/@@p.a.jqt.testPage")
        self.wait()

        sel.click("taform")
        self.wait()
        self.failUnless(sel.is_text_present("Test Form"))
        self.failUnless(sel.is_text_present("exact:ajax_load:"))

        sel.type("Password", "xxx")
        sel.click("//input[@name='Check' and @value='3']")
        sel.click("//input[@name='Radio' and @value='3']")
        sel.click("submitButton")
        self.wait()
        # self.failUnless(sel.is_text_present("exact:Multiple:one"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Name:MyName1"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Single2:A"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Single:one"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Radio:3"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Text:This is Form1"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:submitButton:Submit1"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Hidden:hiddenValue"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Password:xxx"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # try: self.failUnless(sel.is_text_present("exact:Check:3"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # sel.click("//input[@name='submitButton' and @value='Submit2']")
        # try: self.failUnless(sel.is_text_present("exact:submitButton:Submit2"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # sel.click("//button[@name='submitButton']")
        # try: self.failUnless(sel.is_text_present("exact:submitButton:Submit5"))
        # except AssertionError, e: self.verificationErrors.append(str(e))
        # sel.click("submitButton6")
