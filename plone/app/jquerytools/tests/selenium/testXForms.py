from base import SeleniumTestCase
import time


class FormTestCase(SeleniumTestCase):

    def test_afancy_form(self):
        """ test basic form functions on a complex form """

        sel = self.selenium

        self.open("@@p.a.jqt.testPage/", look_for="id=taform")

        sel.click("taform")
        self.waitForElement("div.overlay-ajax form")
        time.sleep(1)
        self.assertTrue(sel.is_text_present("Test Form"))
        self.assertFalse(sel.is_text_present("exact:Should not show"))
        self.assertTrue(sel.is_text_present("exact:ajax_load:"))

        sel.type("Password", "xxx")
        sel.click("//input[@name='Check' and @value='3']")
        sel.click("//input[@name='Radio' and @value='3']")
        sel.click("submitButton")
        time.sleep(3)

        self.assertTrue(sel.is_text_present("exact:ajax_load:"))
        self.assertTrue(sel.is_text_present("exact:Multiple:one"))
        self.assertTrue(sel.is_text_present("exact:Name:MyName1"))
        self.assertTrue(sel.is_text_present("exact:Single2:A"))
        self.assertTrue(sel.is_text_present("exact:Single:one"))
        self.assertTrue(sel.is_text_present("exact:Radio:3"))
        self.assertTrue(sel.is_text_present("exact:Text:This is Form1"))
        self.assertTrue(sel.is_text_present("exact:submitButton:Submit1"))
        self.assertTrue(sel.is_text_present("exact:Hidden:hiddenValue"))
        self.assertTrue(sel.is_text_present("exact:Password:xxx"))
        self.assertTrue(sel.is_text_present("exact:Check:3"))

        # Make sure we can handle other submit methods, and that the
        # value of the submit button is in the request
        sel.click("//input[@name='submitButton' and @value='Submit2']")
        time.sleep(3)
        self.assertTrue(sel.is_text_present("exact:submitButton:Submit2"))
        sel.click("//button[@name='submitButton']")
        time.sleep(3)
        self.assertTrue(sel.is_text_present("exact:submitButton:Submit5"))

        # pushing submit6 should close the overlay
        sel.click("//input[@name='submitButton6']")
        time.sleep(3)
        self.assertFalse(sel.is_text_present("Test Form"))
