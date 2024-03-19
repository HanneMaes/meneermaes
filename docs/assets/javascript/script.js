document.addEventListener("DOMContentLoaded", function() {

    // Add target _blank to all external links
    var links = document.querySelectorAll('a');
    links.forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href.startsWith('http') && !href.includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
        }
    });
    console.log('Added "target: _blank" to all external links:', links);
    
    // Add target _blank to all links in an iframe, so they don't open in the iframe itself
    window.addEventListener('DOMContentLoaded', function () {
        var iframes = document.querySelectorAll('iframe');
        iframes.forEach(function (iframe) {
            iframe.onload = function () {
                var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                var links = iframeDoc.querySelectorAll('a');
                links.forEach(function (link) {
                    link.setAttribute('target', '_blank');
                });
            };
        });
        console.log('Added "target: _blank" to all links in iframes:', iframes);
    });

});

