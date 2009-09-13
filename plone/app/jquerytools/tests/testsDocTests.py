import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


testfiles = (
    'ploneIntegration.txt',
)

ptc.setupPloneSite()


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            f, package = 'plone.app.jquerytools.tests',
            test_class = ptc.FunctionalTestCase,
            optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
        
            for f in testfiles
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
