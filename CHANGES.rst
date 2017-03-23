Changelog
=========

1.9.1 (2017-03-23)
------------------

Bug fixes:

- Updated jquery.form and jquery.tools to latest versions.
  [msom]

1.9.0 (2016-12-02)
------------------

New features:

- An overlay registered by the prepOverlay function can now be optionally be
  triggered by a hover or doubleclick event, instead of click.
  [petri]


1.8.0 (2016-08-12)
------------------

New features:

- The prepOverlay function can be used on a form instead of a link. When a
  button of this form is clicked, the form action attribute is used to retrieve
  the overlay. (This was already the case in previous versions, What's new is
  the following.) If method="POST", the overlay will be fetched via a POST with
  the form payload instead of GET.
  The use of a POST instead of GET may be useful to avoid the url length limit.
  [vincentfretin]


1.7.1 (2016-06-27)
------------------

- Proper clean setup of jquery.form
  [gotcha]


1.7.0 (2015-04-29)
------------------

- Remove the development profile. Unminified resources are still provided. If
  you need them, include them in your own profile.
  [thet]

- Move jQueryTools tooltip into separate file, so that it can be selectively
  disabled.
  [thet]


1.6.2 (2014-11-04)
------------------

- Revert "check each tooltip for existence, fixes issue 349". Fixes broken
  Tooltip.
  [vincentfretin, thet]


1.6.1 (2014-09-11)
------------------

- Fix dateinput (change event was not triggered anymore).
  [thomasdesvenain]


1.6.0 (2014-07-10)
------------------

- Ensure jQuery 1.7+, including 1.9 compatibility by using the dev branch of
  jquerytools and applying further fixes. We now use a fork of jquerytools at:
  https://github.com/collective/jquerytools/tree/dev
  [thet]

- Fix ``overlayhelpers.js`` to work with jQuery 1.7 and 1.9.
  jQuery.buildFragment has a slightly changed API. While it accepts a list of
  context objects in jQuery 1.7, it expects an explicit context object in
  jQuery 1.9. See::

    - https://github.com/jquery/jquery/blob/1.7/src/manipulation.js#L465
    - https://github.com/jquery/jquery/blob/1.7/src/manipulation.js#L472
    - https://github.com/jquery/jquery/blob/1.9.1/src/manipulation.js#L617

  [thet]

- Switched to Grunt based build system.
  [thet]

- Switch test infrastructure to plone.app.testing.
  [sdelcourt]


1.5.7 (2014-02-23)
------------------

- Fix a test isolation issue.
  [davisagli]

- Install plone.app.jquerytools.js after plone_javasscript_variables.js
  in new instances.
  [bloodbare]


1.5.6 (2013-08-13)
------------------

- In the date picker, fire the change event on the input
  so it doesn't bubble up and cause an error in jquery 1.8.
  [davisagli]

- Backport pull-req https://github.com/jquerytools/jquerytools/pull/873 and
  apply in other jquerytools files too: Fix API of outerWidth and outerHeight
  to ensure jQuery 1.8.x compatibility. This change is backwards compatible at
  least to 1.4, since jquerytools used the API incorrectly. See jQuery 1.4 API
  doc:
  http://web.archive.org/web/20100210083046/http://api.jquery.com/outerWidth/
  [thet]

1.5.5 (2013-03-18)
------------------

- Set z-index for dateinput calendar popup so that it will display in
  an overlay context.
  [smcmahon]

- Pass the pbo object as third parameter to the redirect callback. This
  provides the same flexibility for redirect that was added for noform in
  1.5.4.
  [izak]


1.5.4 (2013-03-04)
------------------

- Now execute inline scripts in ajax overlay.
  [vincentfretin]

- Give the pbo object as second parameter for noform callback. You can access
  everything from it, for example the overlay trigger pbo.source.
  [vincentfretin]

- Give the disconnected "el" jQuery object (the div created with the html
  response) instead of "this" (the request object) to the noform and redirect
  callbacks. This fixes the noformerrorshow callback from popupforms.js in the
  Products.CMFPlone package.
  [vincentfretin]

- Adapt jquery.tools.dateinput.css to use Plone popup calendar icon and
  compatible styles.
  [smcmahon]

- Change jqt_checkout_build to *not* pick up dateinput.css from jQuery.
  This should be Plone-specific.
  [smcmahon]


1.5.3 (2013-01-17)
------------------

- Call ploneTabInit when a form is reloaded with errors.
  [vincentfretin]


1.5.2 (2013-01-01)
------------------

- Dont be so strong with regexp in overlayhelpers.js
  [garbas]


1.5.1 (2012-10-16)
------------------

- Revert to always adding the overlay at the bottom of the document body.
  [davisagli]

- Make sure the "Close this box" link has a hiddenStructure class so it
  won't show up for most users.
  [davisagli]


1.5 (2012-08-30)
----------------

- Add translatable string for close box. This and the following change by
  giacomos fix http://dev.plone.org/ticket/12122.
  [fulviocasali]

- Use link instead of @import for css resources. This improves speed, since it
  better uses parallel downloads. See: "don't use @import" by Steve Souders.
  [thet]


1.4 - 2012-05-11
----------------

- Added a link in the close button to improve accessibility
  [giacomos]

- Update to jQueryTools 1.2.7.
  [thet]

- Fix sed command in jqt_checkout_build script to work on Linux and OSX.
  [thet]

- Update to jQueryTools 1.2.6.
  [smcmahon]

- For overlays that are not already inline, insert them inline after the
  triggering element rather than at the end of the body. This solves an
  accessibility problem for screen readers (see ticket #12123), but is
  going to require more css reset work for overlay styling.
  [smcmahon]


1.3 - 2011-06-27
----------------

- Add events triggering so you can hook into it more.
  [vangheem]

- Don't break if a formselector was specified but the overlay has no form.
  [davisagli]

- Refactor setup of AJAX-loaded content so it's easier to call from custom
  code.
  [davisagli]

- It's now possible to repeatedly apply prepOverlay to the same element
  and have the last-applied case win. Previously, once prepOverlay had been
  used on an element, all subsequent uses on that element were ignored.
  [smcmahon]

- Add documentation in README for using jQuery Tools event handlers.
  [smcmahon]


1.2 - 2011-05-13
----------------

- 1.2 final release.
  [esteele]


1.2b5 - 2011-04-06
------------------

- Added next.gif and prev.gif for the dateinput widget.
  [vincentfretin]

- Add ajax_load hidden input to loaded forms.
  [smcmahon]


1.2b4 - 2010-12-05
------------------

- Add plone.app.testing / Selenium testing framework based on esteele's
  example.
  [smcmahon]

- noform and redirect options not passed to ajax form handlers in
  b1, b2, b3. Fixed.
  [smcmahon]


1.2b3 - 2010-12-30
------------------

- Some options not passed to ajax form handlers in b1, b2. Fixed.
  [smcmahon]


1.2b2 - 2010-12-29
------------------

- AJAX overlays broken in b1 due to plain stupidity. Will try to remember
  to always test after editing.
  [smcmahon]


1.2b1 - 2010-12-27
------------------

- Avoid creating overlay divs until needed; remove ajax overlay divs
  on close. Less DOM clutter.
  [smcmahon]

- Include both .min.js and .js versions of js resources to make life
  a little easier for folks who want to read the source. The .min.js
  versions will go into the browser resources.
  [smcmahon]

- Updated documentation so it reflect changes.
  [garbas]

- Updated jquerytools to 1.2.5. dateinput, rangeinput and validator
  plugins added as additional browser resources. Now all plugins from
  jquerytools are added with this package.
  [garbas]

- Added build script which builds js files from source (from github).
  [garbas]

- getContent does not exist in jqtools. It has been replaced by
  getOverlay. http://flowplayer.org/tools/forum/40/28687
  [naro]


1.1.2 - 2010-07-19
------------------

- Avoid use of genericsetup:upgradeSteps (plural), which doesn't work in Plone
  3.
  [davisagli]


1.1.1 - 2010-07-19
------------------

- Add 'description' parameter to upgrade step directives to fix breakage on
  Plone 3.
  [davisagli]


1.1 - 2010-07-18
----------------

- Add overlays.css. For Plone 3 only (it is disabled on installation in Plone
  4, and on upgrade from Plone 3 to Plone 4).
  [davisagli]

- Update license to GPL version 2 only.
  [hannosch]

- Added experimental windmill browser integration tests.
  [smcmahon]


1.1b5 - 2010-06-12
------------------

- Update to jQuery Tools 1.2.3.
  [smcmahon]

- Recode to one "var" per function standard.
  [smcmahon]

- Don't show empty ajax form responses, even if "noform" is not set.
  [smcmahon]


1.1b4 - 2010-06-06
------------------

- The select technique used to filter ajax response in b1-b3 was not robust
  if the responseText was not well-formed (think ZMI forms). Fixed by emulating
  the technique used in jQuery's .load method.
  [smcmahon]


1.1b3 - 2010-06-03
------------------

- Switch back to "find", undoing 1.1b2 change. 'filter' does not find
  descendents, and will thus not work in most validation error situations.
  Also, cleaned up identifiers and comments that suggested that we were
  filtering rather than selecting.
  [smcmahon]


1.1b2 - 2010-06-03
------------------

- Fix regression in filtering introduced in 1.1b1.
  [davisagli]


1.1b1
-----

- Integrate jQuery form plugin http://malsup.com/jquery/form/ so that we
  can handle file uploads. Bump version # to reflect significant change.
  [davisagli, smcmahon]


1.0rc3
------

- Update to tools 1.2.2. (Trivial changes)
  [smcmahon]

- Set max-height on ajax overlays to 75% of the viewport's height; switch
  to fixed positioning on everything but IE6.
  [smcmahon]

- Updated to tools 1.2.1; removed jqt image resources (too bulky
  to justify as part of main distribution).
  [smcmahon]


1.0rc2
------

- Change query string variable for ajax loads from "rand" to "ajax_load"
  to clarify its purpose.

- Added cssclass option for prepOverlay.


1.0rc1
------

- Add responseText to parameters passed in the redirect callback; this
  enables smarter redirects in cases where pages may have disappeared.
  [smcmahon]

- Add 'link-overlay' class to overlay triggers.
  [davisagli]

- Made the closing of an ajax overlay delete the loaded content so that it
  doesn't muddy up the DOM. [smcmahon]

- Added 'source' to data_parent to be able to access source element (element
  on original page, which raised the overlay window) eg. in afterpost handler.
  [naro]

- Add message for ajax no response from server.
  [smcmahon]

- Insert overlays in the DOM at the end of body rather than visual
  portal wrapper. Fixes #10307.
  [smcmahon]


1.0b17
------

- 1.0b16 fix to click-outside-overlay cause *any* click to close the overlay.
  Fixed. [smcmahon]


1.0b16
------

- Patched jquery.tools.min.js to fix close on click outside overlay.
  [smcmahon]

- Improved logic for finding the submit button via a click handler.
  [smcmahon]


1.0b15 - 2010-02-17
-------------------

- AJAX form handling was busted in Safari by submit button marshaling
  fix. Found a hopefully more general solution for finding submit
  button name and value.
  [smcmahon]

- beforepost and afterpost callback options weren't working. fixed.
  [smcmahon]

- Recover when jQuery tries to throw away error responses in ajax loads.
  [smcmahon]

- Circumvent double-submit warning for AJAX forms.
  [smcmahon]

- Use the $ convention for jQuery.
  [smcmahon]


1.0b14 - 2010-10-27
-------------------

- Add beforepost and afterpost callback options for ajax forms.
  [smcmahon]

- Change reload strategy to set location to current href rather than using
  reload, which can cause repost queries on some browsers.
  [smcmahon]


1.0b13 - 2010-01-22
-------------------

- Fixed marshaling of submit buttons on AJAX submit when form has multiple
  buttons.
  [smcmahon]


1.0b12 - 2010-01-11
-------------------

- Allow noform and redirect options to be specified as callback functions.
  This will allow building in more smarts about what to do when ajax
  forms finish.
  [smcmahon]

- Avoid clobbering the onLoad config option if it is passed to prepOverlay.
  [davisagli]


1.0b11 - 2009-12-27
-------------------

- Declared all package dependencies and avoid unused imports inside tests.
  [hannosch]


1.0b10 - 2009-12-18
-------------------

- Add plugins resource and graphics directory.

- Update jqtools to use tooltips 1.1.3


1.0b9
-----

- Avoid overlay helper errors in Plone 3.x when trying to handle tabbed
  forms.


1.0b8
-----

- Check 'action' attribute for url, enabling simple forms to open overlays.


1.0b7
-----

- Initialize form tabbing on ajax form load.

- Marshall submit button values in ajax form submit, since jQuery
  doesn't include them.


1.0b6
-----

- Document use of overlay helper.


1.0b5
-----

- Integrate overlay helpers originally developed in pipbox. These
  provide support for AJAX loads and forms.


1.0b4
-----

- Advance to jQuery Tools 1.2.1


1.0b3
-----

- Fix packaging problem that prevented easy_install of 1.0b2.


1.0b2
-----

- Move to jQuery Tools 1.1.1.


1.0b1
-----

- Initial release
