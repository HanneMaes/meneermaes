document.addEventListener("DOMContentLoaded", function() {

	// give 'opdracht & oefening' headers a CSS-class
	var headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');  // Get all headers
	headers.forEach(function(header) { 									// Loop through each header
		if (header.textContent.trim().startsWith('Opdracht')) { 		// Check if the header's text starts with "opdracht"
			header.classList.add('opdrachtHeader'); 					// If it does, add the class "opdrachtHeader"
		} else if (header.textContent.trim().startsWith('Oefening')) { 		// Check if the header's text starts with "opdracht"
			header.classList.add('oefeningHeader'); 					// If it does, add the class "opdrachtHeader"
		}
	});

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

