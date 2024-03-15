document.addEventListener("DOMContentLoaded", function() {

    // Add target _blank to all external links
    var links = document.querySelectorAll('a');
    links.forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href.startsWith('http') && !href.includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
        }
    });
    
});

