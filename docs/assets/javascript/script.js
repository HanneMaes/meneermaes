document.addEventListener("DOMContentLoaded", function () {

  // variables I need in multiple things
  var headers = document.querySelectorAll("h1, h2, h3, h4, h5, h6"); // Get all headers
  var maxLetters = 50; // Trim text in the sidebar (toc, incoming and outgoind links)

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

  /* ***************** */
  /* TABLE OF CONTENTS */
  /* ***************** */

  var tocHTML = "";

  // Loop through each header
  headers.forEach(function (header) { 

  	// trim text
  	var headerText = header.innerHTML.length > maxLetters ? header.innerHTML.substring(0, maxLetters) + '...' : header.innerHTML;

  	// create HTML
  	tocHTML += '<li class="' + header.localName + 'Link"><a>' + headerText + '<a></li>';

  });
  document.getElementById('toc').innerHTML = tocHTML;

/* ************************* */
/* OUTGOING & INCOMING LINKS */
/* ************************* */

  const currentPath = window.location.pathname;

  // Outgoing links
  // Collect all internal <a> tags inside <article> that point to a different page

  function buildOutgoingLinks() {
    const article = document.querySelector("article");
    if (!article) return;

    const seen = new Set();
    const items = [];

    article.querySelectorAll("a[href]").forEach(function (a) {
      const href = a.getAttribute("href");

      // Skip anchors, external links, and the current page itself
      if (!href || href.startsWith("http") || href.startsWith("#")) return;

      // Normalise: strip query-string / hash, resolve relative paths
      const url = new URL(href, window.location.href);
      const path = url.pathname;

      if (path === currentPath) return;     // skip self
      if (seen.has(path)) return;           // deduplicate
      seen.add(path);

      // Use the link text, or fall back to the last path segment
      const label = a.textContent.trim() ||
        path.split("/").filter(Boolean).pop() ||
        path;

      items.push({ path, label });
    });

    const container = document.getElementById("outgoingLinks");
    if (!container) return;

    if (items.length === 0) {
      container.innerHTML = "";
      return;
    }

    const links = items
      .map(item => `<li><a class="linksOutgoing" href="${item.path}">${item.label}</a></li>`)
      .join("");

    container.innerHTML = links;
  }

  // Incoming links
  // Fetch every page listed in search.json; check its raw HTML for a link to
  // the current page. Show those that reference us.

  async function buildIncomingLinks() {
    const container = document.getElementById("incomingLinks");
    if (!container) return;

    let allPages;
    try {
      const res = await fetch("/search.json");
      allPages = await res.json();
    } catch (e) {
      console.warn("incomingLinks: could not load search.json", e);
      return;
    }

    // Remove the current page from the candidate list
    const candidates = allPages.filter(function (p) {
      if (!p.url) return false;
      const path = new URL(p.url, window.location.href).pathname;
      if (path === currentPath) return false;

      // skip non-content pages
      if (!p.title) return false;                          // pages without a title
      if (path.endsWith(".xml")) return false;
      if (path.endsWith(".json")) return false;
      if (path.endsWith(".txt")) return false;

      return true;
    });
    // Patterns we look for inside the raw HTML of each page
    // (both exact path and with baseurl prefix if your Jekyll site has one)
    const needle = currentPath;                   // e.g.  /content/css/selectors
    const needleEncoded = encodeURI(needle);

    const incomingItems = [];

    // Fetch pages in parallel; cap concurrency so we don't hammer the server
    const BATCH = 6;
    for (let i = 0; i < candidates.length; i += BATCH) {
      const batch = candidates.slice(i, i + BATCH);
      await Promise.all(
        batch.map(async function (page) {
          try {
            const res = await fetch(page.url, { method: "GET" });
            if (!res.ok) return;
            const html = await res.text();

            // A quick string search is enough – we just need href="...currentPath..."
            if (html.includes(needle) || html.includes(needleEncoded)) {
              incomingItems.push({ path: page.url, label: page.title || page.url });
            }
          } catch (_) {
            // Network error on a single page – skip silently
          }
        })
      );
    }

    if (incomingItems.length === 0) {
      container.innerHTML = "";
      return;
    }

    const links = incomingItems
      .map(item => `<li><a class="linksIncoming" href="${item.path}">${item.label}</a></li>`)
      .join("");

    container.innerHTML = links;
  }

  // Run both (outgoing is instant; incoming is async)
  buildOutgoingLinks();
  buildIncomingLinks();

  /* ************* */
  /* TARGET _BLANK */
  /* ************* */

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

  /* ****** */
  /* SEARCH */ 
  /* ****** */

  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  let pages = [];

  fetch('/search.json') // Fetch the search data
    .then(response => response.json())
    .then(data => {
      pages = data;
    });

  searchInput.addEventListener('input', function(e) { // Search function
    const query = e.target.value.toLowerCase();
    
    if (query.length < 2) {
      searchResults.innerHTML = '';
      return;
    }

    const results = pages.filter(page => 
      page.title && page.title.toLowerCase().includes(query)
    );

    displayResults(results);
  });

  function displayResults(results) {
    if (results.length === 0) {
      searchResults.innerHTML = '<p>No results found</p>';
      return;
    }

    const html = results.map(page => 
      `<a href="${page.url}">${page.title}</a>`
    ).join('');
    
    searchResults.innerHTML = html;
  }

});
