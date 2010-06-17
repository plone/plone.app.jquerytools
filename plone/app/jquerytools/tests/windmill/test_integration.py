import unittest
from niteoweb.windmill import WindmillTestCase
from Products.PloneTestCase.setup import setupPloneSite
from Products.PloneTestCase.layer import onsetup
from Products.Five.zcml import load_config
from Testing import ZopeTestCase as ztc

setupPloneSite(products=[])

class IntegrationTestCaseAnon(WindmillTestCase):

    def afterSetUp(self):
        """Setup for each test
        """
        ztc.utils.setupCoreSessions(self.app)
        self.setRoles(['Manager'])
        self.login_user()

    def test_login_popup(self):
        """Check that login form works as popup; if it does, this confirms
           overlays work for unauth users and that the refresh no-form
           action works.
        """
        client = self.wm

        # Log out so that we can test log in
        client.click(link=u'Log out')
        client.waits.forPageLoad(timeout=u'20000')
        client.click(link=u'Home')
        client.waits.forPageLoad(timeout=u'20000')

        # Test that login option is set as an overlay
        client.asserts.assertNode(id=u'anon-personalbar')
        client.asserts.assertNode(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        # click on it, look for overlay
        client.click(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.waits.forElement(jquery=u'("div.pb-ajax #login_form")[0]', timeout=u'1000')
        # make sure that clicking outside dismisses popup
        client.click(id=u'exposeMask')
        client.waits.sleep(milliseconds=u'500')
        client.asserts.assertNotNode(jquery=u'("div.pb-ajax #login_form")[0]')
        
        # open popup again, try submitting empty; look for error.
        # presence of error confirms that we're not losing the portal message
        # in the popup form contents filter.
        client.asserts.assertNode(id=u'anon-personalbar')
        client.asserts.assertNode(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.click(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.waits.forElement(jquery=u'("div.pb-ajax #login_form")[0]', timeout=u'1000')
        client.click(name=u'submit')
        client.waits.forElement(jquery=u"('div.pb-ajax dl .portalMessage .error dt')", timeout=u'1000')
        
        # try again with real login
        client.type(text=u'portal_owner', id=u'__ac_name')
        client.type(text=u'secret', id=u'__ac_password')
        client.click(name=u'submit')
        # expect a page load
        client.waits.forPageLoad(timeout=u'20000')
        client.asserts.assertNode(id=u'portal-personaltools')
        
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)