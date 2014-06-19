from Products.CMFCore.utils import getToolByName
try:
    from plone.app.upgrade import v40  # nopep8
    HAS_PLONE40 = True
except ImportError:
    HAS_PLONE40 = False


def disable_css(context):
    cssreg = getToolByName(context, 'portal_css')
    res = cssreg.getResource('++resource++plone.app.jquerytools.overlays.css')
    if res is not None:
        res.setEnabled(False)


def importVarious(gscontext):
    # don't run as a step for other profiles
    if gscontext.readDataFile('is_jquerytools_profile.txt') is None:
        return

    site = gscontext.getSite()
    if HAS_PLONE40:
        # in Plone 4, we don't need overlays.css
        disable_css(site)
