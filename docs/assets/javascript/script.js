document.addEventListener("DOMContentLoaded", function () {
  // variables I need in multiple things
  var headers = document.querySelectorAll("h1, h2, h3, h4, h5, h6"); // Get all headers

  /* ************************ */
  /* ADD CSS CLASSES TO STUFF */
  /* ************************ */

  // give 'opdracht & oefening' headers a CSS-class
  headers.forEach(function (header) {
    // Loop through each header
    if (header.textContent.trim().startsWith("Opdracht")) {
      // Check if the header's text starts with "opdracht"
      header.classList.add("opdrachtHeader"); // If it does, add the class "opdrachtHeader"
    } else if (header.textContent.trim().startsWith("Oefening")) {
      // Check if the header's text starts with "opdracht"
      header.classList.add("oefeningHeader"); // If it does, add the class "opdrachtHeader"
    }
  });

  /* **************** */
  /* SMOOTH SCROLLING */
  /* **************** */
  
  // This css code: scroll-behavior: smooth; /* smooth scrolling for anchor links
  // Only works for anchor links on the page, and I want them to also work when going to another page

  window.addEventListener('load', function() { // Check if URL has a hash on page load
    if (window.location.hash) {
      const target = document.querySelector(window.location.hash);
      if (target) {
        setTimeout(() => {
          target.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    }
  });
  
  /* ***************** */
  /* TABLE OF CONTENTS */
  /* ***************** */

  // var tocHTML = "";
  // console.log("TOC");
  // headers.forEach(function (header) { // Loop through each header

  // 	// trim text
  // 	var maxLetters = 40;
  // 	var headerText = header.innerHTML.length > maxLetters ? header.innerHTML.substring(0, maxLetters) + '...' : header.innerHTML;

  // 	// create HTML
  // 	tocHTML += '<a class="' + header.localName + 'Link">' + headerText + '<a><br>';
  // });
  // document.getElementById('toc').innerHTML = tocHTML;

  /* ************ */
  /* TARGET BLANK */
  /* ************ */

  // Add target _blank to all external links
  var links = document.querySelectorAll("a");
  links.forEach(function (link) {
    var href = link.getAttribute("href");
    if (
      href &&
      href.startsWith("http") &&
      !href.includes(window.location.hostname)
    ) {
      link.setAttribute("target", "_blank");
    }
  });
  console.log('Added "target: _blank" to all external links:', links);

  // Add target _blank to all links to .pdf files
  document.querySelectorAll('a[href$=".pdf"]').forEach((link) => {
    link.setAttribute("target", "_blank");
  });
  console.log('Added "target: _blank" to all .pdf links:', links);

  // Add target _blank to all links in an iframe, so they don't open in the iframe itself
  window.addEventListener("DOMContentLoaded", function () {
    var iframes = document.querySelectorAll("iframe");
    iframes.forEach(function (iframe) {
      iframe.onload = function () {
        var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        var links = iframeDoc.querySelectorAll("a");
        links.forEach(function (link) {
          link.setAttribute("target", "_blank");
        });
      };
    });
    console.log('Added "target: _blank" to all links in iframes:', iframes);
  });

  /* ******************************** */
  /* HIDE BREADCRUMBS ON HIDDEN PAGES */
  /* ******************************** */

  // Check if the URL contains the '/hidden/'
  if (window.location.href.includes("/hidden/")) {
    document.querySelector(".breadcrumbs").style.display = "none";
  }

  /* ***************** */
  /* ANIMATE OS SCROLL */ 
  /* ***************** */

  // H1
  document.querySelectorAll('h1').forEach(function(h1) {
    h1.setAttribute('data-aos', 'fade-right');
  });

  // callout
  document.querySelectorAll('.callout').forEach(function(callout) {
    callout.setAttribute('data-aos', 'zoom-out');
  });

  // blockquote
  document.querySelectorAll('blockquote p').forEach(function(bq) {
    bq.setAttribute('data-aos', 'zoom-in');
  });

  // Initialize AOS AFTER adding attributes
  AOS.init({
    duration: 1000,
    once: true
  });

  /* ******************** */
  /* HEADING ANCHOR LINKS */
  /* ******************** */

  // Add anchor links to h1 and h2 tags
  document.querySelectorAll('h1, h2').forEach(function(heading) {
    if (!heading.id) { // Create an ID from the heading text if it doesn't have one
      heading.id = heading.textContent
        .trim()
        .toLowerCase()
        .replace(/[^\w\s-]/g, '') // Remove special characters
        .replace(/\s+/g, '-')     // Replace spaces with hyphens
        .replace(/--+/g, '-');    // Replace multiple hyphens with single
    }
    
    // Create the link icon
    var link = document.createElement('a');
    link.href = '#' + heading.id;
    link.className = 'heading-anchor';
    link.innerHTML = '←'
    link.title = 'Link to this section';
    
    // Add the link to the heading
    heading.appendChild(link);
  });

});
