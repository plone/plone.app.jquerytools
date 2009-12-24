import unittest
import doctest

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc

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
