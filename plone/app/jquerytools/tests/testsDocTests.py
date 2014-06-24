from plone.app.jquerytools.testing import PAJQT_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest

optionflags = doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE


def test_suite():
    return unittest.TestSuite([
        layered(
            doctest.DocFileSuite(
                'tests/ploneIntegration.txt',
                package='plone.app.jquerytools',
                optionflags=optionflags),
            layer=PAJQT_FUNCTIONAL_TESTING)
    ])
