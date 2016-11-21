Introduction
============

plone.app.jquerytools adds `jquery.tools`_ and some related
overlay and form-handling JavaScript libraries to Plone.

``plone.app.jquerytools`` was developed for Plone 4. Earlier versions could
be used in Plone 3.x by adding a zcml slug and running its
GS Setup extension profile. This version requires Plone 4.x.

Plone developers will wish to use ``plone.app.jquerytools`` to provide DOM
popups, particularly if they require AJAX. There is extensive support
for AJAX form posting. It's also useful for adding dateinput and forminput
widgets that are HTML5 compatible.

The AJAX and AJAX-form support is Plone-specific, and is documented in this module.
Dateinput, rangeinput, accordions, and tooltips are all unchanged from
jquerytools, and the jquerytools docs should be consulted.

.. contents::


Development
===========

Since version 2.0 we use a Grunt based build system. To update the package, you
have to setup Grunt like descibed below (this works on Linux). You need ``npm``
and ``git`` installed.

If grunt-cli isn't installed, do::

    $ sudo npm install -g grunt-cli

Then install the rest locally::

    $ npm install

For more information see: http://gruntjs.com/getting-started


Available resources
===================

`jquery.tools`_ plugins and widgets are packed into Zope browser resources:

``++resource++plone.app.jquerytools.js``
    Default plugins and widgets used by plone. This resource is enabled
    by default with ``plone.app.jquerytools:default`` profile.

    Included scripts: `overlay.js`_, `scrollable.js`_, `tabs.js`_,
    `toolbox.history.js`_, `toolbox.expose.js`_, `tooltip.js`_

``++resource++plone.app.jquerytools.plugins.js``
    Additional plugin and widgets which does not take much space and for
    this reason are packed together. This plugins are not enabled by
    default.

    Included scripts: `overlay.apple.js`_, `scrollable.autoscroll.js`_,
    `scrollable.navigator.js`_, `tabs.slideshow.js`_, `toolbox.flashembed.js`_,
    `toolbox.mousewheel.js`_, `tooltip.dynamic.js`_, `tooltip.slide.js`_

``++resource++plone.app.jquerytools.dateinput.js`` ``++resource++plone.app.jquerytools.dateinput.css``
    `jquerytools dateinput`_ widget with style from `first demo`_. Both
    scripts are added to portal_javascript and portal_css but disabled by
    default.

``++resource++plone.app.jquerytools.rangeinput.js``
    `jquerytools rangeinput`_ widget. Added to portal_javascript tool, but
    disabled by default.

``++resource++plone.app.jquerytools.validator.js``
    `jquerytools validator`_ script, which should help you with nice
    validation of your forms. Added to portal_javascript tool, but
    disabled byt default.

``++resource++plone.app.jquerytools.form.js``
    Integrates the `jquery form plugin`_ to add support for AJAX form
     handling. More about this below.

``++resource++plone.app.jquerytools.overlayhelpers.js``
    not yet minimized) and ``++resource++plone.app.jquerytools.overlays.css``
    (Size: 1.9KB, not yet minimized)

    Adds helper code for loading overlays dynamically and for handling AJAX
    forms based on existing pages with minimal setup. More about this in
    instructions below.

JS resources are minified, but uncompressed versions are available in
plone/app/jquerytools/browser for reading/debugging purposes. To use them
for debugging, edit plone/app/jquerytools/configure.zcml to temporarily
specify files ending with .js rather than .min.js.


Overlay helpers
===============

plone.app.jquerytools provides a helper for handling various kinds of dynamic
overlays, including overlays with forms you wish handled by AJAX.

The helper, jQuery.fn.prepOverlay, is a jQuery-style function: it should be
used as a method of a jQuery selection object. The selection object is always
a selection of trigger elements.

prepOverlay should be passed one parameter: a options object, which will often
be constructed as a JavaScript literal object.


Examples
--------

Let's say, for example, that you want to make clicking on news-item photos
open a lightbox-style larger version of the image. To do this, you'll need to
specify:

* A jQuery style selector for a Plone element, e.g., ".newsImageContainer a"

* "image" for the load method ("ajax" and "iframe" are other alternatives)

* A regular expression search/replace to transform the href or src URL.
  In this example, we're changing the URL to point to the preview-sized
  image. So, our search/replace pair is "/image_view_fullscreen"
  and "_preview".

* You could also specify additional overlay configuration parameters.

The code::

    $('.newsImageContainer a')
        .prepOverlay({
             subtype: 'image',
             urlmatch: '/image_view_fullscreen$',
             urlreplace: '_preview'
            });

What if you want the lightbox-style larger image to open upon doubleclick or
hover, instead? Just add a "event" attribute to override the default::

    $('.newsImageContainer a')
        .prepOverlay({
             subtype: 'image',
             urlmatch: '/image_view_fullscreen$',
             urlreplace: '_preview',
             event: 'dblclick'
            });

The optional "event" attribute takes one of three values: either the default
"click", "dblclick", or "hover".

Another quick example, one that provides full-image popups for images placed
via kupu::

    $('img.image-right, img.image-left, img.image-inline')
        .prepOverlay({
            subtype: 'image',
            urlmatch: '/image_.+$',
            urlreplace: ''
            });

What's different? We're targeting <img ... /> tags, which don't have href
attributes. The helper automatically picks up the target URL from the src
attribute, so that we can have a popup view of image elements that aren't
linked to that view. Note also that we're using a real regular expression
in the search/replace so that we can strip off image_preview, image_mini, etc.

And, a configuration to put the site map in an iframe popup with expose
settings, picking up the target from an href::

    $('#siteaction-sitemap a')
        .prepOverlay({
            subtype: 'iframe',
            config: {expose:{color:'#00f'}}
            });

Options
-------

The complete options list:

subtype
  'image' | 'iframe' | 'ajax'
urlmatch:
  Regular expression for a portion of the target URL. Target
  URL is determined by checking href, src or action attributes.
urlreplace
  Replacement expression for the matched expression.
filter (ajax only)
  the jQuery selector used to find the elements of
  the ajax loaded resource that you wish to use in the overlay.
width
  Width of the popup. Defaults to 60%. Overriden by image width
  for image overlays. Percentages are computed against window width,
  not parent.
cssclass
  A custom css class to apply to the overlay. Ignored
  for inline overlays.
config
  jQuery Tools configuration options in a dictionary.

For AJAX overlay forms, add the following, form-oriented, options:

formselector
  Used to specify the JQuery selector for any
  forms inside the loaded content that you want to be handled
  inside the overlay by doing an AJAX load to get the overlay
  content.

  When a form is submitted, the overlay handler checks the response
  for formselector. If it's found, the result is displayed in the
  overlay and form handlers are bound. If not, the 'noform' action
  is carried out.

noform
  the action to take if an ajax form is submitted and the returned
  content has nothing matching the formselector. Available actions include
  'close' to simply close the overlay, 'reload' to reload the page, and
  'redirect' to redirect to another page. If you choose 'redirect', you
  must specify the URL in the redirect option. Default
  action is to display the filtered response in the popup.

  You may also supply as the 'noform' argument a
  callback function that returns one of these strings. The overlay helper
  will call the function with the overlay element as an argument.

closeselector
  use this to specify a JQuery selector that will be used
  to find elements within the overlay that should close the overlay if
  clicked. The most obvious example is a form's cancel button.

redirect
  if you specify 'redirect' for the noform action, use the
  redirect option to specify the full target URL. You may also supply a
  callback function that returns a URL. The overlay helper will call the
  function with the overlay element and the response text as arguments.

beforepost
  you may specify a function that will be called before the
  AJAX form posting. This callback will be passed the jQuery-wrapped form
  and the serialized form data. Return true if you wish the AJAX form
  handler to handle the event; return false if you wish to cancel the
  submit.

afterpost
  you may specify a function that will be called immediately
  after the AJAX load of the post response. The function will be passed an
  element containing the returned HTML as a jQuery object. Second argument
  is data_parent object, which contains overlay configuration and other
  useful data in the jQuery 'data' resource. This callback occurs before
  any other processing of the response. The callback function's return
  value is ignored.

AJAX
----

Some of the options allow use of AJAX to get content. When you're
loading content into an overlay or tab via AJAX, you're nearly always
going to want only part of the loaded content. For example, if you're
picking up a Plone page, you may only want the #content div's contents.

To do this, just add a CSS (or JQuery) selector as a 'filter' option.
JQuery's load method (which pipbox uses) will only pick up the content inside
the selection.

For example, let's say that you wish to display the standard Plone site map
in an overlay. You could use::

    $('#siteaction-sitemap a').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *'
        });

The filter code causes the overlay handler to load only a portion of the
AJAX-loaded HTML into the overlay, picking up only what's inside the
#content div. If you don't specify a filter, you'll get
everything inside the body section of the page -- not usually what you
want.

Some browsers cache AJAX loads, so a random argument is automatically
added to URLs.

NOTE: the  "ajax_load" query string argument is automatically added to AJAX
urls and may be used in templates to determine which resources are shipped
for AJAX overlays. Plone 4's main template uses this to exclude nearly
all elements of the page outside the content area.


AJAX Forms
----------

The overlay helper can automatically handle forms that are within the
overlay by making an AJAX post action, then replacing the overlay content with
the results.

Specify forms for this handling with the "formselector" option. The content
filter specified in the original overlay is reused.

For example, if you wished to handle the standard Plone contact form in an
overlay, you could specify::

    $('#siteaction-contact a').prepOverlay({
        subtype: 'ajax',
        filter: '#content>*',
        formselector: 'form'
        });

Another example: using popups for the delete confirmation and rename forms
(from the action menu)::

    $('a#delete,a#rename').prepOverlay({
        subtype: 'ajax',
        filter: '#content>*',
        closeselector: '[name=form.button.Cancel]'
        });

There are a couple of differences here. First, there is no form selector
specified; that's because we don't want to install an ajax submit handler
when we may be renaming or deleting the displayed object. Second, we specify
a close selector so that pushing the cancel button will close the overlay
without bothering to submit the form.

See ``Products/CMFPlone/skins/plone_ecmascript/popupforms.js`` for several
examples of using callbacks to handle tricky cases like confirming deletion of
the current content item.

The `jquery form plugin`_ is used to do the data serialization for form posts.
It provides a more complete serialization, including submit name/value and file
data, than jQuery alone.

The prepOverlay function can be used on a form instead of a link. When a button
of this form is clicked, the form action attribute is used to retrieve the
overlay. If method="POST", the overlay will be fetched via a POST with the
form payload instead of GET.
The use of a POST instead of GET may be useful to avoid the url length limit.

jQuery Tools Events
-------------------

Event handlers for jQuery Tools overlay events may be set in via the optional
"config" argument, which is passed as a dictionary. For example, to specify an
onBeforeLoad event::

    $('a#testimage').prepOverlay({
        subtype: 'image',
        config: {
            onBeforeLoad : function (e) {
                console.log('onBeforeLoad', this.getOverlay());
                return true;
                }
            }
        });


Useful events are specified in the jQuery Tools `overlay documentation`_.
Also, see the `events documentation`_. Note that you should return ``true`` in
```onBeforeLoad``` and ``onBeforeClose`` handlers if you want the default behavior
(opening or closing). Return ``false`` to prevent opening or closing.

jQuery Tools passes the event as a parameter when it calls the event handlers.
``this`` will be the jqt API object, which has ``getOverlay()`` and
``getTrigger()`` methods.


.. _`jquery.tools`: http://jquerytools.github.io
.. _`overlay.js`: http://jquerytools.github.io/documentation/overlay/index.html
.. _`scrollable.js`: http://jquerytools.github.io/documentation/scrollable/index.html
.. _`tabs.js`: http://jquerytools.github.io/documentation/tabs/index.html
.. _`toolbox.history.js`: http://jquerytools.github.io/documentation/toolbox/history.html
.. _`toolbox.expose.js`: http://jquerytools.github.io/documentation/toolbox/expose.html
.. _`tooltip.js`: http://jquerytools.github.io/documentation/tooltip/index.html
.. _`overlay.apple.js`: http://jquerytools.github.io/documentation/overlay/apple.html
.. _`scrollable.autoscroll.js`: http://jquerytools.github.io/documentation/scrollable/autoscroll.html
.. _`scrollable.navigator.js`: http://jquerytools.github.io/documentation/scrollable/navigator.html
.. _`tabs.slideshow.js`: http://jquerytools.github.io/documentation/tabs/slideshow.html
.. _`toolbox.flashembed.js`: http://jquerytools.github.io/documentation/toolbox/flashembed.html
.. _`toolbox.mousewheel.js`: http://jquerytools.github.io/documentation/toolbox/mousewheel.html
.. _`tooltip.dynamic.js`: http://jquerytools.github.io/documentation/tooltip/dynamic.html
.. _`tooltip.slide.js`: http://jquerytools.github.io/documentation/tooltip/slide.html
.. _`jquerytools dateinput`: http://jquerytools.github.io/documentation/dateinput/index.html
.. _`first demo`: http://jquerytools.github.io/demos/dateinput/index.html
.. _`jquerytools rangeinput`: http://jquerytools.github.io/documentation/rangeinput/index.html
.. _`jquerytools validator`: http://jquerytools.github.io/documentation/validator/index.html
.. _`jquery form plugin`: http://malsup.com/jquery/form
.. _`overlay documentation`: http://jquerytools.github.io/documentation/overlay/#events
.. _`events documentation`: http://jquerytools.github.io/documentation/scripting.html#events
