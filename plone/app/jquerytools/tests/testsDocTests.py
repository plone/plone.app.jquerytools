import unittest
import doctest

from plone.app.jquerytools.testing import PLONEAPPJQUERYTPOOLS_FUNCTIONAL_TESTING

from plone.testing import layered


def test_suite():
    return unittest.TestSuite(
        [layered(doctest.DocFileSuite('tests/ploneIntegration.txt', package='plone.app.jquerytools',
         optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE),
         layer=PLONEAPPJQUERYTPOOLS_FUNCTIONAL_TESTING)]
    )
