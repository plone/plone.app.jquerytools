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
        client = self.wm

        # Log out so that we can test log in
        client.click(link=u'Log out')
        client.waits.forPageLoad(timeout=u'20000')
        client.click(link=u'Home')
        client.waits.forPageLoad(timeout=u'20000')

        client.asserts.assertNode(id=u'anon-personalbar')
        client.asserts.assertNode(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.click(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.waits.forElement(jquery=u'("div.pb-ajax #login_form")[0]', timeout=u'1000')
        client.click(id=u'exposeMask')
        client.waits.sleep(milliseconds=u'500')
        client.asserts.assertNotNode(jquery=u'("div.pb-ajax #login_form")[0]')
        client.asserts.assertNode(id=u'anon-personalbar')
        client.asserts.assertNode(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.click(jquery=u'("#anon-personalbar a.link-overlay")[0]')
        client.waits.forElement(jquery=u'("div.pb-ajax #login_form")[0]', timeout=u'1000')
        client.click(name=u'submit')
        client.waits.forElement(jquery=u"('div.pb-ajax dl .portalMessage .error dt')", timeout=u'1000')
        client.type(text=u'portal_owner', id=u'__ac_name')
        client.type(text=u'secret', id=u'__ac_password')
        client.click(name=u'submit')
        client.waits.forPageLoad(timeout=u'20000')
        client.asserts.assertNode(id=u'portal-personaltools')
        # client.click(link=u'Log out')
        # client.waits.forPageLoad(timeout=u'20000')
        # self.setRoles(['Manager'])
        
        # log back in for other tests
        # self.login_user()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)