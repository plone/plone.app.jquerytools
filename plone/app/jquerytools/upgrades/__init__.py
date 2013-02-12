from Products.CMFCore.utils import getToolByName

def run_all_import_steps(context):
    context = getToolByName(context, "portal_setup")
    context.runAllImportStepFromProfile(
        'profile-plone.app.jquerytools:default',
        purge_old=False)
