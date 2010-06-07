/*****************

   jQuery Tools overlay helpers.

   Copyright © 2010, The Plone Foundation
   Licensed under the GPL, see LICENSE.txt for details.

*****************/

/*jslint browser: true, onevar: true, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, newcap: true, immed: true */
/*global jQuery, ajax_noresponse_message, window */

// Name space object for pipbox
var pb = {spinner:{}};

// We may be creating multiple targets per page. We need to be able to
// tell them apart. We'll do it by counting.
pb.overlay_counter = 1;

jQuery.tools.overlay.conf.oneInstance = false;

jQuery(function($) {

    pb.spinner.show = function () {
        $('body').css('cursor','wait');
    };
    pb.spinner.hide = function () {
        $('body').css('cursor','');
    };

    /******
        $.fn.prepOverlay jQuery plugin to inject overlay target into DOM and
        annotate it with the data we'll need in order to display it.
    ******/
    $.fn.prepOverlay = function(pbo) {
        return this.each(function() {
            var o, config, onBeforeLoad, onLoad, src, nt,
                el, selector, parts;

            o = $(this);

            // set overlay configuration
            config = pbo.config || {};

            // set onBeforeLoad handler
            onBeforeLoad = pb[pbo.subtype];
            if (onBeforeLoad) {
                config.onBeforeLoad = onBeforeLoad;
            }
            onLoad = config.onLoad;
            config.onLoad = function() {
                if (onLoad) {
                    onLoad.apply(this, arguments);
                }
                pb.fi_focus(this.getOverlay());
            };

            // if there's a rel attribute, we've already
            // visited this node.
            if (!o.attr('rel')) {
                // be promiscuous, pick up the url from
                // href, src or action attributes
                src = o.attr('href') || o.attr('src') || o.attr('action');

                // translate url with config specifications
                if (pbo.urlmatch) {
                    src = src.replace(new RegExp(pbo.urlmatch), pbo.urlreplace);
                }

                if (pbo.subtype === 'inline') {
                    // we're going to let tools' overlay do all the real
                    // work. Just get the markers in place.
                    src = src.replace(/^.+#/, '#');
                    $("[id='" + src.replace('#', '') + "']")
                        .addClass('overlay');
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
                    nt = 'pb_' + pb.overlay_counter;
                    pb.overlay_counter += 1;

                    // mark the source with a rel attribute so we can find
                    // the overlay, and a special class for styling
                    o.attr('rel', '#' + nt);
                    o.addClass('link-overlay');

                    // create a target element; a div with markers;
                    // content will be inserted here by the callback
                    el = $(
                    '<div id="' + nt +
                        '" class="overlay overlay-' + pbo.subtype +
                        ' ' + (pbo.cssclass || '') +
                        '"><div class="close"><span>Close</span></div>'
                    );

                    // add the target element at the end of the body.
                    el.appendTo($("body"));

                    // if we've a width specified, set it on the overlay div
                    if (pbo.width) {
                        el.width(pbo.width);
                    }

                    // We'll need the selector in the callback/click, so let's
                    // store it on the target element.
                    //
                    // A selector may have been supplied in options, otherwise
                    // anything in src after a space is going to be a
                    // $ selector to use in an ajax load so that
                    // we don't get a whole page.
                    selector = pbo.filter || pbo.selector;
                    if (!selector) {
                        // see if one's been supplied in the src
                        parts = src.split(' ');
                        src = parts.shift();
                        selector = parts.join(' ');
                    }
                    el.data('target', src).data('selector', selector);

                    // are we being asked to handle forms in an ajax overlay?
                    // save the form selector on the target element.
                    el.data('formtarget', pbo.formselector);
                    el.data('noform', pbo.noform);
                    el.data('redir_url', pbo.redirect);
                    el.data('closeselector', pbo.closeselector);
                    el.data('beforepost', pbo.beforepost);
                    el.data('afterpost', pbo.afterpost);
                    // o = jquery element which raised the overlay window.
                    el.data('source', o);

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
                    default:
                        throw "Unsupported overlay type";
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
        var content, api, src, img, el;

        // find target container
        content = $($(this).attr('rel'));
        // and its JQT api
        api = content.overlay();

        // is the image loaded yet?
        if (content.find('img').length === 0) {
            // load the image. first, get the
            // src information out of the stored data.
            src = content.data('target');
            if (src) {
                pb.spinner.show();

                // create the image and stuff it
                // into our target
                img = new Image();
                img.src = src;
                el = $(img);
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
        pb.fi_focus
        First-input focus inside $ selection.
    ******/
    pb.fi_focus = function(jqo) {
        if (! jqo.find("form div.error :input:first").focus().length) {
            jqo.find("form :input:visible:first").focus();
        }
    };


    /******
        pb.ajax_error_recover
        jQuery's ajax load function does not load error responses.
        This routine returns the cooked error response.
    ******/
    pb.ajax_error_recover = function(responseText, selector) {
        var tcontent = $('<div/>')
            .append(responseText.replace(/<script(.|\s)*?\/script>/gi, ""));
        return selector ? tcontent.find(selector) : tcontent;
    };


    /******
        pb.prep_ajax_form
        Set up form with ajaxForm, including success and error handlers.
    ******/
    pb.prep_ajax_form = function(form) {
        var ajax_parent = form.closest('.pb-ajax'),
            data_parent = ajax_parent.closest('.overlay-ajax'),
            formtarget = data_parent.data('formtarget'),
            closeselector = data_parent.data('closeselector'),
            beforepost = data_parent.data('beforepost'),
            afterpost = data_parent.data('afterpost'),
            api = data_parent.overlay(),
            selector = data_parent.data('selector'),
            options = {};

        options.beforeSerialize = function() {
            pb.spinner.show();
        };

        if (beforepost) {
            options.beforeSubmit = function(arr, form, options) {
                return beforepost(form, arr, options);
            };
        }
        options.success = function(responseText, statusText, xhr, form) {
            // success comes in many forms, some of which are errors;
            //

            var noform, el, myform, success, target;

            success = statusText === "success" || statusText === "notmodified";

            if (! success) {
                // The responseText parameter is actually xhr
                responseText = responseText.responseText;
            }
            // strip inline script tags
            responseText = responseText.replace(/<script(.|\s)*?\/script>/gi, "");

            // create a div containing the optionally filtered response
            el = $('<div />').append(
                selector ?
                    // a lesson learned from the jQuery source: $(responseText)
                    // will not work well unless responseText is well-formed;
                    // appending to a div is more robust, and automagically
                    // removes the html/head/body outer tagging.
                    $('<div />').append(responseText).find(selector)
                    :
                    responseText
                );

            // afterpost callback
            if (success && afterpost) {
                afterpost(el, data_parent);
            }

            myform = el.find(formtarget);
            if (success && myform.length) {
                ajax_parent.empty().append(el);
                pb.fi_focus(ajax_parent);

                // attach submit handler with the same options
                myform.ajaxForm(options);

                // attach close to element id'd by closeselector
                if (closeselector) {
                    el.find(closeselector).click(function(event) {
                        api.close();
                        return false;
                    });
                }
            } else {
                // there's no form in our new content or there's been an error
                if (success) {
                    noform = data_parent.data('noform');
                    if (typeof(noform) === "function") {
                        // get action from callback
                        noform = noform(this);
                    }
                } else {
                    noform = statusText;
                }


                switch (noform) {
                case 'close':
                    api.close();
                    break;
                case 'reload':
                    api.close();
                    pb.spinner.show();
                    // location.reload results in a repost
                    // dialog in some browsers; very unlikely to
                    // be what we want.
                    location.replace(location.href);
                    break;
                case 'redirect':
                    api.close();
                    pb.spinner.show();
                    target = data_parent.data('redir_url');
                    if (typeof(target) === "function") {
                        // get target from callback
                        target = target(this, responseText);
                    }
                    location.replace(target);
                    break;
                default:
                    if (el.children()) {
                        // show what we've got
                        ajax_parent.empty().append(el);
                    } else {
                        api.close();
                    }
                }
            }
            pb.spinner.hide();
        };
        // error and success callbacks are the same
        options.error = options.success;
        form.ajaxForm(options);
    };



    /******
        pb.ajax_click
        Click handler for ajax sources. The job of this routine
        is to do the ajax load of the overlay element, then
        call the JQT overlay loader.
    ******/
    pb.ajax_click = function(event) {
        var content = $($(this).attr('rel')),
            api = content.overlay(),
            src = content.data('target'),
            el = content.children('div.pb-ajax'),
            selector = content.data('selector'),
            formtarget = content.data('formtarget'),
            closeselector = content.data('closeselector'),
            sep;

        pb.spinner.show();

        // prevent double click warning for this form
        $(this).find("input.submitting").removeClass('submitting');

        // see if we already have a container to load
        if (!el.length) {
            // we don't, so create it
            el = $('<div class="pb-ajax" />');
            if (api.getConf().fixed) {
                // don't let it be over 75% of the viewport's height
                el.css('max-height', Math.floor($(window).height() * 0.75));
            }
            content.append(el);
        }

        // affix a random query argument to prevent
        // loading from browser cache
        sep = (src.indexOf('?') >= 0) ? '&': '?';
        src += sep + "ajax_load=" + (new Date().getTime());

        // add selector, if any
        if (selector) {
            src += ' ' + selector;
        }

        // and load the div
        el.load(src, null, function(responseText, errorText) {
            var el = $(this);

            if (errorText === 'error') {
                el.append(pb.ajax_error_recover(responseText, selector));
            } else if (!responseText.length) {
                el.append(ajax_noresponse_message || 'No response from server.');
            }

            // a non-semantic div here will make sure we can
            // do enough formatting.
            el.wrapInner('<div />');

            // add the submit handler if we've a formtarget
            if (formtarget) {
                pb.prep_ajax_form(el.find(formtarget));
            }

            // if a closeselector has been specified, tie it to the overlay's
            // close method via closure
            if (closeselector) {
                el.find(closeselector).click(function(event) {
                    api.close();
                    return false;
                });
            }

            // This may be a complex form.
            if ($.fn.ploneTabInit) {
                el.ploneTabInit();
            }

            // remove element on close so that it doesn't congest the DOM
            api.onClose = function () { el.remove(); };

            // Now, it's all ready to display; hide the
            // spinner and call JQT overlay load.
            pb.spinner.hide();
            api.load();

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
        var content = this.getContent(),
            src;

        pb.spinner.show();

        if (content.find('iframe').length === 0) {
            src = content.data('target');
            if (src) {
                content.append(
                '<iframe src="' + src + '" width="' +
                 content.width() + '" height="' + content.height() + 
                 '" onload="pb.spinner.hide()"/>'
                );
            }
        } else {
            pb.spinner.hide();
        }
        return true;
    };


});
