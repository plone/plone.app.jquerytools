import unittest_jshint


class JSHintTestCase(unittest_jshint.JSHintTestCase):

    include = (
        'plone.app.jquerytools:browser',
        )

    exclude = (
        'jquery.form.js',
        'jquery.form.min.js',
        'jquery.tools.dateinput.css',
        'jquery.tools.dateinput.js',
        'jquery.tools.dateinput.min.js',
        'jquery.tools.js',
        'jquery.tools.min.js',
        'jquery.tools.plugins.js',
        'jquery.tools.plugins.min.js',
        'jquery.tools.rangeinput.js',
        'jquery.tools.rangeinput.min.js',
        'jquery.tools.validator.js',
        'jquery.tools.validator.min.js',
        )
