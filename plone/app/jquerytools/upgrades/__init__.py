from Products.CMFCore.utils import getToolByName


def null_upgrade_step(context):
    pass


def upgrade1to2(context):
    # run the custom import step (and cssregistry dependency) to install
    # overlays.css on Plone 3
    context = getToolByName(context, "portal_setup")
    context.runImportStepFromProfile(
        'profile-plone.app.jquerytools:default',
        'jquerytools-various',
        purge_old=False)


def common_upgrade(context):
    """ Common upgrade for newer jquerytools versions - import javascript
    registry and cook resources.
    """
    setup = getToolByName(context, "portal_setup")
    setup.runImportStepFromProfile(
        'profile-plone.app.jquerytools:default',
        'jsregistry')
    tool = getToolByName(context, 'portal_javascripts')
    tool.cookResources()
