from plone.app.jquerytools.testing import PLONEAPPJQUERYTPOOLS_FUNCTIONAL_TESTING  # nopep8
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
            layer=PLONEAPPJQUERYTPOOLS_FUNCTIONAL_TESTING)
    ])
