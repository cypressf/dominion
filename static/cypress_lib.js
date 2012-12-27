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
            console.debug(s);
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

    // put it in the global namespace
    window._ = library;
})();