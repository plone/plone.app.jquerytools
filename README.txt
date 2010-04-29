Introduction
============

plone.app.jquerytools does four things:

* It adds jQuery Tools to Plone's JavaScript resources.

* It adds some helper code for loading overlays dynamically and
  for handling AJAX forms.

* Adds several jQuery Tools plugins to the JavaScript resources.
  The plugins registry entry is disabled by default. Applications
  that need it and can justify a little more js bloat may turn it on.

  Plugins included are:

  tools.tabs.slideshow, tools.tabs.history, tools.tooltip.slide
  tools.tooltip.dynamic
  tools.scrollable.circular, tools.scrollable.autoscroll, tools.scrollable.navigator,
  tools.overlay.gallery-1.0.0

* Makes the jQuery Tools graphics available in a browser resource directory,
  ++resource++plone.app.jquerytools.graphics. For example, the black.png file
  is ++resource++plone.app.jquerytools.graphics/black.png.

For information on using jQuery tools, see http://flowplayer.org/tools/ .

plone.app.jquerytools was developed for Plone 4. However, it can
be used in Plone 3.x by adding a zcml slug and running it's
GS Setup extension profile, or by adding a product like Products.pipbox
that will load the GS profile for you.

Overlay Helpers
---------------

plone.app.jquerytools provides a helper for handling various kinds of dynamic
overlays, including overlays with forms you wish handled by AJAX.

The helper, jQuery.fn.prepOverlay, is a jQuery-style function: it should be
used as a method of a jQuery selection object. The selection object is always
a selection of trigger elements.

prepOverlay should be passed one parameter: a options object, which will often
be constructed as a Javascript literal object.

Overlay examples
----------------

Let's say, for example, that you want to make clicking on news-item photos
open a lightbox-style larger version of the image. To do this, you'll need to
specify:

 * A jquery style selector for a Plone element, e.g., ".newsImageContainer a"

 * "image" for the load method ("ajax" and "iframe" are other alternatives)

 * A regular expression search/replace to transform the href or src URL.
   In this example, we're changing the URL to point to the preview-sized
   image. So, our search/replace pair is "/image_view_fullscreen"
   and "_preview".

 * You could also specify additional overlay configuration parameters.

The code::

    jq('.newsImageContainer a')
        .prepOverlay({
             subtype:'image',
             urlmatch:'/image_view_fullscreen$',
             urlreplace:'_preview'
            });

Another quick example, one that provides full-image popups for images placed
via kupu::

    jq('img.image-right,img.image-left,img.image-inline')
        .prepOverlay({
            subtype:'image',
            urlmatch:'/image_.+$',
            urlreplace:''
            });

What's different? We're targeting <img ... /> tags, which don't have href
attributes. the helper picks up the target URL from the src attribute, so that
we can have a popup view of image elements that aren't linked to that view.
Note also that we're using a real regular expression in the search/replace so
that we can strip off image_preview, image_mini, etc.

And, a configuration to put the site map in an iframe popup with expose
settings, picking up the target from an href::

    jq('#siteaction-sitemap a')
        .prepOverlay({
            subtype:'iframe',
            config:{expose:{color:'#00f'}}
            });

Options
-------

The complete options list:

 * subtype: 'image' | 'iframe' | 'ajax'

 * selector: the JQuery selector to find your elements

 * urlmatch: Regular expression for a portion of the target URL

 * urlreplace: Replacement expression for the matched expression

 * width: Width of the popup. Leave unset to determine through CSS.
   Overriden by image width for image overlays.
 
 * cssclass: A custom css class to apply to the overlay. Ignored
   for inline overlays.

 * config: JQuery Tools configuration options in a dictionary

For AJAX overlays, add the following, form-oriented, options:

    * formselector: Used to specify the JQuery selector for any
      forms inside the loaded content that you want to be handled
      inside the overlay by doing an AJAX load to replace the overlay
      content.

    * noform: the action to take if an ajax form is submitted and the returned
      content has nothing matching the formselector. Available actions include
      'close' to simply close the overlay, 'reload' to reload the page, and
      'redirect' to redirect to another page. If you choose 'redirect', you
      must specify the URL in the redirect option. You may also supply a callback
      function that returns one of these strings. The overlay helper will call
      the function with the overlay element as an argument.

    * closeselector: use this to specify a JQuery selector that will be used
      to find elements within the overlay that should close the overlay if
      clicked. The most obvious example is a form's cancel button.

    * redirect: if you specify 'redirect' for the noform action, use the
      redirect option to specify the full target URL. You may also supply a callback
      function that returns a URL. The overlay helper will call
      the function with the overlay element and the response text as arguments.

    * beforepost: you may specify a function that will be called before the
      AJAX form posting. The form submit event is passed to the function.
      Return true if you wish the AJAX form handler to handle the event;
      return false if you wish the default submit action to occur instead.

    * afterpost: you may specify a function that will be called immediately
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

To do this, just add a CSS (or JQuery) selector to the target URL.
JQuery's load method (which pipbox uses) will only pick up the content inside
the selection.

For example, let's say that you wish to display the standard Plone site map
in an overlay. You could use::

    jq('#siteaction-sitemap a').prepOverlay({
        subtype:'ajax',
        urlmatch:'$',urlreplace:' #content > *'
        });

The urlmatch/urlreplace code adds a selector to the end of the URL when it
calls JQuery's load to get the content, picking up only what's inside the
#content div.

If you don't specify a selection from the loaded page's DOM, you'll get
everything inside the body section of the page.

Some browsers cache AJAX loads, so a random argument is added to URLs.


AJAX Forms
----------

The overlay helper can automatically handle having forms that are within the
overlay by making an AJAX post action, then replacing the overlay content with
the results.

Specify forms for this handling with the "formselector" option. The content
filter specified in the original overlay is reused.

For example, if you wished to handle the standard Plone contact form in an
overlay, you could specify::

    jq('#siteaction-contact a').prepOverlay({
        subtype:'ajax',
        urlmatch:'$', urlreplace:' #content>*',
        formselector:'form'
        });

Another example: using popups for the delete confirmation and rename forms
(from the action menu)::

    jq('a#delete,a#rename').prepOverlay({
        subtype:'ajax',
        urlmatch:'$', urlreplace:' #region-content',
        'closeselector':'[name=form.button.Cancel]'
        });

There are a couple of differences here. First, there is no form selector
specified; that's because we don't want to install an ajax submit handler
when we may be renaming or deleting the displayed object. Second, we specify
a close selector so that pushing the cancel button will close the overlay
without bothering to submit the form.

See Products/CMFPlone/skins/plone_ecmascript/popupform.js for several examples
of using callbacks to handle tricky cases.

Limitations: Forms may not include file fields, as the current marshaling
strategy isn't adequate to deal with them.