module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        shell: {
            cleanup_jquerytools: {
                command: 'rm -Rf repo-jquerytools',
            },
            cleanup_jqueryform: {
                command: 'rm -Rf repo-jqueryform',
            },
            gitclone_jquerytools: {
                command: 'git clone --branch dev git@github.com:collective/jquerytools.git repo-jquerytools',
            },
            gitclone_jqueryform: {
                command: 'git clone --branch master git@github.com:malsup/form.git repo-jqueryform',
            }
        },

        concat: {
            options: {
                separator: grunt.util.linefeed + grunt.util.linefeed
            },
            jquerytools: {
                src: [
                    'repo-jquerytools/src/overlay/overlay.js',
                    'repo-jquerytools/src/scrollable/scrollable.js',
                    'repo-jquerytools/src/tabs/tabs.js',
                    'repo-jquerytools/src/toolbox/toolbox.history.js',
                    'repo-jquerytools/src/toolbox/toolbox.expose.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.js'
            },
            jquerytools_plugins: {
                src: [
                    'repo-jquerytools/src/overlay/overlay.apple.js',
                    'repo-jquerytools/src/scrollable/scrollable.autoscroll.js',
                    'repo-jquerytools/src/scrollable/scrollable.navigator.js',
                    'repo-jquerytools/src/tabs/tabs.slideshow.js',
                    'repo-jquerytools/src/toolbox/toolbox.flashembed.js',
                    'repo-jquerytools/src/toolbox/toolbox.mousewheel.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.plugins.js'
            },
            jquerytools_tooltip: {
                src: [
                    'repo-jquerytools/src/tooltip/tooltip.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.tooltip.js'
            },
            jquerytools_tooltip_plugins: {
                src: [
                    'repo-jquerytools/src/tooltip/tooltip.dynamic.js',
                    'repo-jquerytools/src/tooltip/tooltip.slide.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.tooltip.plugins.js'
            },
            jquerytools_dateinput: {
                src: [
                    'repo-jquerytools/src/dateinput/dateinput.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.dateinput.js'
            },
            jquerytools_rangeinput: {
                src: [
                    'repo-jquerytools/src/rangeinput/rangeinput.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.rangeinput.js'
            },
            jquerytools_validator: {
                src: [
                    'repo-jquerytools/src/validator/validator.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.tools.validator.js'
            },
            jquerytools_form: {
                src: [
                    'repo-jqueryform/jquery.form.js',
                ],
                dest: 'plone/app/jquerytools/browser/jquery.form.js'
            },
        },

        uglify: {
            options: {
                mangle: false
            },
            jquery_form: {
                files: {
                    'plone/app/jquerytools/browser/jquery.form.min.js': ['plone/app/jquerytools/browser/jquery.form.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.tooltip.min.js': ['plone/app/jquerytools/browser/jquery.tools.tooltip.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.tooltip.plugins.min.js': ['plone/app/jquerytools/browser/jquery.tools.tooltip.plugins.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.dateinput.min.js': ['plone/app/jquerytools/browser/jquery.tools.dateinput.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.min.js': ['plone/app/jquerytools/browser/jquery.tools.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.rangeinput.min.js': ['plone/app/jquerytools/browser/jquery.tools.rangeinput.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.validator.min.js': ['plone/app/jquerytools/browser/jquery.tools.validator.js', ],
                    'plone/app/jquerytools/browser/jquery.tools.plugins.min.js': ['plone/app/jquerytools/browser/jquery.tools.plugins.js', ],
                }
            },
        }

    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-shell');

    // Default task(s).
    grunt.registerTask('default', ['shell', 'concat', 'uglify']);
    grunt.registerTask('update', ['concat', 'uglify']);
};
