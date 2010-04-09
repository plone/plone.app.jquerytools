/*****************

   jQuery Tools overlay helpers.

   Copyright © 2009, The Plone Foundation
   Licensed under the GPL

*****************/



// Name space object for pipbox
var pb = {spinner:{}};

// We may be creating multiple targets per page. We need to be able to
// tell them apart. We'll do it by counting.
pb.overlay_counter = 1;

jQuery.tools.overlay.conf.oneInstance = false;

(function($) {

    pb.spinner.show = function () {
        $('body').css('cursor','wait');
    };
    pb.spinner.hide = function () {
        $('body').css('cursor','');
    };

    /******
        $.fn.prepOverlay
        jQuery plugin to inject overlay target into DOM
        and annotate it with the data we'll need in order
        to display it.
    ******/
    $.fn.prepOverlay = function(pbo) {
        return this.each(function() {
            var o = $(this);

            // set overlay configuration
            var config = pbo.config || {};

            // set onBeforeLoad handler
            var onBeforeLoad = pb[pbo.subtype];
            if (onBeforeLoad) {
                config.onBeforeLoad = onBeforeLoad;
            }
            var onLoad = config.onLoad;
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
                var src = o.attr('href') || o.attr('src') || o.attr('action');

                // translate url with config specifications
                if (pbo.urlmatch) {
                    src = src.replace(RegExp(pbo.urlmatch), pbo.urlreplace);
                }

                if (pbo.subtype == 'inline') {
                    // we're going to let tools' overlay do all the real
                    // work. Just get the markers in place.
                    src = src.replace(RegExp('^.+#'), '#');
                    $("[id='" + src.replace('#', '') + "']").addClass('overlay');
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
                    // the overlay, and a special class for styling
                    o.attr('rel', '#' + nt);
                    o.addClass('link-overlay');

                    // create a target element; a div with markers;
                    // content will be inserted here by the callback
                    var el = $(
                    '<div id="' + nt + '" class="overlay overlay-' + pbo.subtype + '">' +
                    '<div class="close"><span>Close</span></div>'
                    );

                    // add the target element at the end of the body.
                    el.appendTo($("body"));

                    // if we've a width specified, set it on the overlay div
                    if (pbo.width) {
                        el.width(pbo.width);
                    }

                    // We'll need the filter in the callback/click, so let's
                    // store it on the target element.
                    //
                    // Filter may have been supplied in options, otherwise
                    // anything in src after a space is going to be a
                    // $ filter to use in an ajax load so that
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
        var content = $($(this).attr('rel'));
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
                var el = $(img);
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
        This routine returns the filtered error response.
    ******/
    pb.ajax_error_recover = function(responseText, filter) {
        var tcontent = $('<div/>').append(responseText.replace(/<script(.|\s)*?\/script>/gi, ""));
        return filter ? tcontent.find(filter) : tcontent;
    };


    /******
        pb.prep_ajax_form
        submit events don't know what caused the submit, but many form
        handlers need to know what button was pushed. We handle this
        by setting a click handler on the form that will annotate the form
        with the name of the clicked button.
    ******/
    pb.prep_ajax_form = function(myform) {
        myform
            .submit(pb.form_handler)
            .click(function(e) {
                var target = $(e.target);
        		if ((target.is(":submit"))) {
        		    this.submitclick = target;
        		}
        		return true;
        	});
    };

    /******
        pb.form_handler
        Submit event handler for AJAX overlay forms.
        It does an ajax post of the form data, then
        uses the response to load the overlay target
        element.
    ******/
    pb.form_handler = function(event) {
        var form = $(event.target);
        var ajax_parent = form.closest('.pb-ajax');
        var data_parent = ajax_parent.closest('.overlay-ajax');
        var formtarget = data_parent.data('formtarget');
        var closeselector = data_parent.data('closeselector');
        var beforepost = data_parent.data('beforepost');
        var afterpost = data_parent.data('afterpost');
        var api = data_parent.overlay();
        var filter = data_parent.data('filter');

        if ($.inArray(form[0], ajax_parent.find(formtarget)) < 0) {
            // this form wasn't ours; do the default action.
            return true;
        }

        // beforepost callback
        if (beforepost) {
            if (! beforepost(event)) {
                return true;
            }
        }

        pb.spinner.show();

        var url = form.attr('action');
        if (filter)
            var url = url + ' ' + filter;
        var inputs = form.serializeArray();

        // jq's serialization does not include the submit button,
        // which zope/plone often need.
        if (this.submitclick) {
            inputs[inputs.length] = {name:this.submitclick.attr('name'), value:this.submitclick.val()};
        }

        // Note that we're loading into a new div (not yet in the DOM)
        // so that we can check it's contents before inserting
        $('<div />').load(url, inputs, function(responseText, errorText) {
            var el = $(this);

            if (errorText === 'error') {
                el.append(pb.ajax_error_recover(responseText, filter));
            }

            // afterpost callback
            if (afterpost) {
                afterpost(el, data_parent);
            }

            pb.spinner.hide();

            var myform = el.find(formtarget);
            if (myform.length) {
                // attach submit handler
                pb.prep_ajax_form(myform);
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

                var noform = data_parent.data('noform');
                if (typeof(noform) == "function") {
                    // get action from callback
                    noform = noform(this);
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
                    var target = data_parent.data('redir_url');
                    if (typeof(target) == "function") {
                        // get target from callback
                        target = target(this, responseText);
                    }
                    location.replace(target);
                    break;
                default:
                    ajax_parent.empty().append(el);
                }
            }
        });

        event.preventDefault();
        return false;
    };


    /******
        pb.ajax_click
        Click handler for ajax sources. The job of this routine
        is to do the ajax load of the overlay element, then
        call the JQT overlay loader.
    ******/
    pb.ajax_click = function(event) {
        var content = $($(this).attr('rel'));
        var api = content.overlay();
        var src = content.data('target');
        var el = content.children('div.pb-ajax');
        var filter = content.data('filter');
        var formtarget = content.data('formtarget');
        var closeselector = content.data('closeselector');

        pb.spinner.show();

        // prevent double click warning for this form
        $(this).find("input.submitting").removeClass('submitting');

        // see if we already have a container to load
        if (!el.length) {
            // we don't, so create it
            el = $('<div class="pb-ajax" />');
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
        el.load(src, null, function(responseText, errorText) {
            var el = $(this);

            if (errorText === 'error') {
                el.append(pb.ajax_error_recover(responseText, filter));
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
            api.onClose = function () { el.remove() };

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


})(jQuery);
