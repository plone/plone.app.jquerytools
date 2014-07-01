from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting


PLONEAPPJQUERYTPOOLS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PloneSandboxLayer(),),
    name="PloneAppJquerytools:Functional")
