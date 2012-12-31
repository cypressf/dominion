// Cypress Library
(function(){
    // object we'll store our functions in
    var library = {};

    library.print = function(s) {
        console.log(s);
    };

    var debug_flag = true;

    library.debug = function(s) {
        if ( debug_flag ) {
            console.debug ? console.debug(s) : console.log(s);
        }
    }

    library.set_debug = function(bool) {
        debug_flag = bool;
    }

    library.get_debug = function() {
        return debug_flag;
    }

    library.http_request = function() {
        if (window.XMLHttpRequest) { // Mozilla, Safari, ...
            return new XMLHttpRequest();
        } else if (window.ActiveXObject) { // IE 8 and older
            return new ActiveXObject("Microsoft.XMLHTTP");
        }
        return false;
    }

    library.set_cookie = function(name, value, days) {
        if (days) {
            var date = new Date();
            date.setTime(date.getTime()+(days*24*60*60*1000));
            var expires = "; expires="+date.toGMTString();
        }
        else var expires = "";
        document.cookie = name+"="+value+expires+"; path=/";
    }

    library.get_cookie = function(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }

    library.delete_cookie = function(name) {
        this.set_cookie(name,"",-1);
    }

    library.escape_html = function(s) {
        var entityMap = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': '&quot;',
            "'": '&#39;',
            "/": '&#x2F;'
        };

        return String(s).replace(/[&<>"'\/]/g, function (s) {
            return entityMap[s];
        });
    }

    // put it in the global namespace
    window._ = library;
})();