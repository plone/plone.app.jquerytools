/*****************

   jQuery Tools overlay helpers.
   
   Copyright © 2009, The Plone Foundation
   Licensed under the GPL

*****************/



// Name space object for pipbox
pb = {};

// We may be creating multiple targets per page. We need to be able to
// tell them apart. We'll do it by counting.
pb.overlay_counter = 1;
// find our spinner; which isn't in the DOM yet, on page load
jQuery(function() {
    pb.spinner = jQuery('#kss-spinner');
});


/******
    jQuery.fn.prepOverlay
    JQuery plugin to inject overlay target into DOM
    and annotate it with the data we'll need in order
    to display it.
******/
jQuery.fn.prepOverlay = function(pbo) {
    return this.each(function() {
        var o = jQuery(this);

        // set overlay configuration
        var config = pbo.config || {};

        // set onBeforeLoad handler
        var onBeforeLoad = pb[pbo.subtype];
        if (onBeforeLoad) {
            config.onBeforeLoad = onBeforeLoad;
        }
        config.onLoad = function() {
            pb.fi_focus(this.getOverlay());
        };

        // if there's a rel attribute, we've already
        // visited this node.
        if (!o.attr('rel')) {
            // be promiscuous, pick up the url from
            //href, src or action attributes
            var src = o.attr('href') || o.attr('src') || o.attr('action');

            // translate url with config specifications
            if (pbo.urlmatch) {
                src = src.replace(RegExp(pbo.urlmatch), pbo.urlreplace);
            }

            if (pbo.subtype == 'inline') {
                // we're going to let tools' overlay do all the real
                // work. Just get the markers in place.
                src = src.replace(RegExp('^.+#'), '#');
                jQuery("[id='" + src.replace('#', '') + "']").addClass('overlay');
                o.removeAttr('href').attr('rel', src);
                // use overlay on the source (clickable) element
                o.overlay();
            } else {
                // we're going to create the container for the overlay,
                // save various bits of information from the pbo options,
                // and enable the overlay.

                // this is not inline, so in one fashion or another
                // we'll be loading it via the beforeLoad callback.
                // create a unique id for a target element
                var nt = 'pb_' + pb.overlay_counter;
                pb.overlay_counter += 1;

                // mark the source with a rel attribute so we can find
                // the overlay
                o.attr('rel', '#' + nt);

                // create a target element; a div with markers;
                // content will be inserted here by the callback
                var el = jQuery(
                '<div id="' + nt + '" class="overlay overlay-' + pbo.subtype + '">' +
                '<div class="close"><span>Close</span></div>'
                );

                // add the target element at the end of the portal wrapper
                // or body.
                var container = jQuery("#visual-portal-wrapper");
                if (!container.length) {
                    container = jQuery("body");
                }
                el.appendTo(container);


                // if we've a width specified, set it on the overlay div
                if (pbo.width) {
                    el.width(pbo.width);
                }

                // We'll need the filter in the callback/click, so let's
                // store it on the target element.
                //
                // Filter may have been supplied in options, otherwise
                // anything in src after a space is going to be a
                // jQuery filter to use in an ajax load so that
                // we don't get a whole page.
                var filter = pbo.filter;
                if (!filter) {
                    // see if one's been supplied in the src 
                    var parts = src.split(' ');
                    src = parts.shift();
                    filter = parts.join(' ');
                }
                el.data('target', src).data('filter', filter);

                // are we being asked to handle forms in an ajax overlay?
                // save the form selector on the target element.
                el.data('formtarget', pbo.formselector);
                el.data('noform', pbo.noform);
                el.data('redir_url', pbo.redirect);
                el.data('closeselector', pbo.closeselector);

                // for some subtypes, we're setting click handlers
                // and attaching overlay to the target element. That's
                // so we'll know the dimensions early.
                // Others, like iframe, just use overlay.
                switch (pbo.subtype) {
                case 'image':
                    o.click(pb.image_click);
                    el.overlay(config);
                    break;
                case 'ajax':
                    o.click(pb.ajax_click);
                    el.overlay(config);
                    break;
                case 'iframe':
                    o.overlay(config);
                    break;
                }

                // in case the click source wasn't
                // already a link.
                o.css('cursor', 'pointer');
            }
        }
    });
};


/******
    pb.image_click
    click handler for ajax sources.
******/
pb.image_click = function(event) {
    // find target container
    var content = jQuery(jQuery(this).attr('rel'));
    // and its JQT api
    var api = content.overlay();

    // is the image loaded yet?
    if (content.find('img').length === 0) {
        // load the image. first, get the
        // src information out of the stored data.
        var src = content.data('target');
        if (src) {
            pb.spinner.show();

            // create the image and stuff it
            // into our target
            var img = new Image();
            img.src = src;
            var el = jQuery(img);
            content.append(el.addClass('pb-image'));

            // Now, we'll cause the overlay to
            // load when the image is loaded.
            el.load( function() {
                pb.spinner.hide();
                api.load();
            });

        }
    } else {
        api.load();
    }

    return false;
};


/******
    pb.close_handler
    when we're in an event, we don't necessarily have
    easy access to the overlay object to use its close
    method.
    This is an alternate.
******/
pb.close_handler = function(event) {
    jQuery(event.target).closest('.overlay').find('.close').click();
    // avoid form submit
    return false;
};


/******
    pb.fi_focus
    First-input focus inside jQuery selection.
******/
pb.fi_focus = function(jqo) {
    if (! jqo.find("form div.error :input:first").focus().length) {
        jqo.find("form :input:visible:first").focus();
    }
};


/******
    pb.form_handler
    submit event handler for AJAX overlay forms.
    It does an ajax post of the form data, then
    uses the response to load the overlay target
    element.
******/
pb.form_handler = function(event) {
    var form = jQuery(event.target);
    var ajax_parent = form.closest('.pb-ajax');
    var formtarget = ajax_parent.data('formtarget');
    var closeselector = ajax_parent.data('closeselector');
    var api = ajax_parent.parent().overlay();

    if (jQuery.inArray(form[0], ajax_parent.find(formtarget)) < 0) {
        // this form wasn't ours; do the default action.
        return true;
    }

    pb.spinner.show();

    var url = form.attr('action') + ' ' + ajax_parent.data('filter');
    var inputs = form.serializeArray();

    // jq's serialization does not include the submit button,
    // which zope/plone often need.
    var submitButton = form.find("input[type=submit]");
    if (submitButton.length) {
        var name = submitButton[0].name;
        if (name) {
            inputs[inputs.length] = {name:name, value:submitButton[0].value};
        }
    }

    // Note that we're loading into a new div (not yet in the DOM)
    // so that we can check it's contents before inserting
    jQuery('<div />').load(url, inputs, function() {
        var el = jQuery(this);

        pb.spinner.hide();

        var myform = el.find(formtarget);
        if (myform.length) {
            // attach submit handler
            myform.submit(pb.form_handler);
            // attach close to element id'd by closeselector
            if (closeselector) {
                el.find(closeselector).click(function(event) {
                    api.close();
                    return false;
                });
            }
            ajax_parent.empty().append(el);
            pb.fi_focus(ajax_parent);
        } else {
            // there's no form in our new content
            switch (ajax_parent.data('noform')) {
            case 'close':
                api.close();
                break;
            case 'reload':
                api.close();
                pb.spinner.show();
                location.reload();
                break;
            case 'redirect':
                api.close();
                pb.spinner.show();
                location.replace(ajax_parent.data('redir_url'));
                break;
            default:
                ajax_parent.empty().append(el);
            }
        }
    });

    return false;
};


/******
    pb.ajax_click
    click handler for ajax sources. The job of this routine
    is to do the ajax load of the overlay element, then
    call the JQT overlay loader.
******/
pb.ajax_click = function(event) {
    var content = jQuery(jQuery(this).attr('rel'));
    var src = content.data('target');
    var el = content.children('div.pb-ajax');
    var filter = content.data('filter');
    var formtarget = content.data('formtarget');
    var closeselector = content.data('closeselector');

    pb.spinner.show();

    // see if we already have a container to load
    if (!el.length) {
        // we don't, so create it, annotating it
        // with the information we'll need if it's
        // got an embedded forms.
        el = jQuery('<div class="pb-ajax" />');
        el.data('filter', filter);
        el.data('formtarget', formtarget);
        el.data('noform', content.data('noform'));
        el.data('redir_url', content.data('redir_url'));

        content.append(el);
    }

    // affix a random query argument to prevent
    // loading from browser cache
    var sep = (src.indexOf('?') >= 0) ? '&': '?';
    src += sep + "rand=" + (new Date().getTime());

    // add filter, if any
    if (filter) {
        src += ' ' + filter;
    }

    // and load the div
    el.load(src, null, function() {
        // a non-semantic div here will make sure we can
        // do enough formatting.
        jQuery(this).wrapInner('<div />');

        // add the submit handler if we've a formtarget
        if (formtarget) {
            el.find(formtarget).submit(pb.form_handler);
        }
        // if a closeselector has been specified, tie it to the overlay's
        // close method via closure
        if (closeselector) {
            el.find(closeselector).click(function(event) {
                content.overlay().close();
                return false;
            });
        }

        // This may be a complex form.
        if (ploneFormTabbing) {
            ploneFormTabbing.initialize();
        }

        // Now, it's all ready to display; hide the
        // spinner and call JQT overlay load.
        pb.spinner.hide();
        content.overlay().load();

        return true;
    });

    // don't do the default action
    return false;
};


/******
    pb.iframe
    onBeforeLoad handler for iframe overlays.

    Note that the spinner is handled a little differently
    so that we can keep it displayed while the iframe's
    content is loading.
******/
pb.iframe = function() {
    pb.spinner.show();

    var content = this.getContent();
    if (content.find('iframe').length === 0) {
        var src = content.data('target');
        if (src) {
            content.append(
            '<iframe src="' + src + '" width="' + content.width() + '" height="' + content.height() + '" onload="pb.spinner.hide()"/>'
            );
        }
    } else {
        pb.spinner.hide();
    }
    return true;
};
