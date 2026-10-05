document.addEventListener("DOMContentLoaded", function () {

  /* ******************** */
  /* GEDEELDE VARIABELEN  */
  /* ******************** */

  const headers = document.querySelectorAll("h1, h2, h3, h4, h5, h6");
  const maxLetters = 30; // Tekst inkorten in de sidebar (toc, in- en uitgaande links)
  const SEARCH_URL = "/search.json"; // Pas aan als je site een baseurl heeft
  const currentPath = normalizePath(window.location.pathname);

  /* ******* */
  /* HELPERS */
  /* ******* */

  // Escape tekst voor veilig gebruik in innerHTML
  function escapeHTML(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  // Tekst inkorten
  function truncate(text) {
    return text.length > maxLetters ? text.substring(0, maxLetters) + "..." : text;
  }

  // Maak paden vergelijkbaar: decode, zonder index.html / .html / slash op het einde
  function normalizePath(path) {
    try {
      path = decodeURI(path);
    } catch (_) {}
    path = path.replace(/index\.html$/, "").replace(/\.html$/, "");
    if (path.length > 1) path = path.replace(/\/+$/, "");
    return path || "/";
  }

  // Id maken uit tekst
  function slugify(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/--+/g, "-");
  }

  // search.json één keer ophalen en hergebruiken
  let searchPromise = null;
  function loadSearchData() {
    if (!searchPromise) {
      searchPromise = fetch(SEARCH_URL)
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        })
        .catch(function (e) {
          console.warn("Kon search.json niet laden", e);
          return [];
        });
    }
    return searchPromise;
  }

  /* ************************ */
  /* ADD CSS CLASSES TO STUFF */
  /* ************************ */

  // Geef 'opdracht' en 'oefening' headers een CSS-class
  headers.forEach(function (header) {
    const text = header.textContent.trim().toLowerCase();
    if (text.startsWith("opdracht")) {
      header.classList.add("opdrachtHeader");
    } else if (text.startsWith("oefening")) {
      header.classList.add("oefeningHeader");
    }
  });

  /* ******************************** */
  /* IDS VOOR ALLE HEADERS (voor toc) */
  /* ******************************** */

  const usedIds = new Set(
    Array.from(document.querySelectorAll("[id]")).map(function (el) {
      return el.id;
    })
  );

  headers.forEach(function (header) {
    if (header.id) return;
    const base = slugify(header.textContent) || "sectie";
    let id = base;
    let n = 2;
    while (usedIds.has(id)) {
      id = base + "-" + n++;
    }
    usedIds.add(id);
    header.id = id;
  });

  /* ***************** */
  /* TABLE OF CONTENTS */
  /* ***************** */

  const toc = document.getElementById("toc");
  if (toc) {
    let tocHTML = "";

    headers.forEach(function (header) {
      const headerText = truncate(header.textContent.trim());
      tocHTML +=
        '<li class="' + header.localName + 'Link">' +
        '<a href="#' + encodeURIComponent(header.id) + '">' + escapeHTML(headerText) + "</a>" +
        "</li>";
    });

    toc.innerHTML = tocHTML;
  }

  /* ************************* */
  /* OUTGOING & INCOMING LINKS */
  /* ************************* */

  // Outgoing links: interne links in <article> naar een andere pagina
  function buildOutgoingLinks() {
    const article = document.querySelector("article");
    const container = document.getElementById("outgoingLinks");
    if (!article || !container) return;

    const seen = new Set();
    const items = [];

    article.querySelectorAll("a[href]").forEach(function (a) {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("#")) return;

      let url;
      try {
        url = new URL(href, window.location.href);
      } catch (_) {
        return;
      }

      // Alleen interne links (slaat http(s) extern, mailto:, tel: enz. over)
      if (url.origin !== window.location.origin) return;

      const path = normalizePath(url.pathname);
      if (path === currentPath) return; // zichzelf overslaan
      if (seen.has(path)) return;       // ontdubbelen
      seen.add(path);

      const label =
        a.textContent.trim() ||
        path.split("/").filter(Boolean).pop() ||
        path;

      items.push({ href: url.pathname, label: truncate(label) });
    });

    container.innerHTML = items
      .map(function (item) {
        return (
          '<li><a class="linksOutgoing" href="' + escapeHTML(item.href) + '">' +
          escapeHTML(item.label) + "</a></li>"
        );
      })
      .join("");
  }

  // Incoming links: pagina's uit search.json die naar de huidige pagina linken
  async function buildIncomingLinks() {
    const container = document.getElementById("incomingLinks");
    if (!container) return;

    const allPages = await loadSearchData();

    const candidates = allPages.filter(function (p) {
      if (!p.url || !p.title) return false;
      const path = new URL(p.url, window.location.href).pathname;
      if (normalizePath(path) === currentPath) return false;
      if (/\.(xml|json|txt)$/.test(path)) return false;
      return true;
    });

    const incomingItems = [];
    const parser = new DOMParser();
    const BATCH = 6; // beperk het aantal gelijktijdige requests

    for (let i = 0; i < candidates.length; i += BATCH) {
      const batch = candidates.slice(i, i + BATCH);

      const results = await Promise.all(
        batch.map(async function (page) {
          try {
            const res = await fetch(page.url);
            if (!res.ok) return null;
            const html = await res.text();
            const doc = parser.parseFromString(html, "text/html");

            // Zoek enkel in de inhoud (niet in menu/sidebar), echte <a href>'s
            const scope = doc.querySelector("article") || doc;
            const base = new URL(page.url, window.location.href);

            const linksHere = Array.from(scope.querySelectorAll("a[href]")).some(
              function (a) {
                const href = a.getAttribute("href");
                if (!href || href.startsWith("#")) return false;
                try {
                  const target = new URL(href, base);
                  return (
                    target.origin === window.location.origin &&
                    normalizePath(target.pathname) === currentPath
                  );
                } catch (_) {
                  return false;
                }
              }
            );

            return linksHere ? { href: page.url, label: page.title } : null;
          } catch (_) {
            return null; // netwerkfout op één pagina: stilletjes overslaan
          }
        })
      );

      results.forEach(function (r) {
        if (r) incomingItems.push(r);
      });
    }

    // Vaste volgorde, ongeacht welke fetch het eerst klaar was
    incomingItems.sort(function (a, b) {
      return a.label.localeCompare(b.label, "nl");
    });

    container.innerHTML = incomingItems
      .map(function (item) {
        return (
          '<li><a class="linksIncoming" href="' + escapeHTML(item.href) + '">' +
          escapeHTML(truncate(item.label)) + "</a></li>"
        );
      })
      .join("");
  }

  buildOutgoingLinks();
  buildIncomingLinks();

  /* ************* */
  /* TARGET _BLANK */
  /* ************* */

  // Externe links en pdf's openen in een nieuw tabblad
  document.querySelectorAll("a[href]").forEach(function (link) {
    const href = link.getAttribute("href");
    let isExternal = false;
    try {
      const url = new URL(href, window.location.href);
      isExternal =
        (url.protocol === "http:" || url.protocol === "https:") &&
        url.origin !== window.location.origin;
    } catch (_) {}

    const isPdf = /\.pdf($|[?#])/i.test(href);

    if (isExternal || isPdf) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    }
  });

  // Links in (same-origin) iframes openen ook in een nieuw tabblad
  document.querySelectorAll("iframe").forEach(function (iframe) {
    function applyTargets() {
      try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        if (!iframeDoc) return;
        iframeDoc.querySelectorAll("a").forEach(function (link) {
          link.setAttribute("target", "_blank");
        });
      } catch (_) {
        // cross-origin iframe: geen toegang, overslaan
      }
    }
    applyTargets();                              // al geladen?
    iframe.addEventListener("load", applyTargets); // of nog niet
  });

  /* ******************************** */
  /* HIDE BREADCRUMBS ON HIDDEN PAGES */
  /* ******************************** */

  if (window.location.href.includes("/hidden/")) {
    const breadcrumbs = document.querySelector(".breadcrumbs");
    if (breadcrumbs) breadcrumbs.style.display = "none";
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

  // Anchor-links bij h1 en h2 (ids bestaan al, zie hierboven)
  document.querySelectorAll("h1, h2").forEach(function (heading) {
    const link = document.createElement("a");
    link.href = "#" + heading.id;
    link.className = "heading-anchor";
    link.textContent = "←";
    link.title = "Link to this section";
    heading.appendChild(link);
  });

  /* ****** */
  /* SEARCH */
  /* ****** */

  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  if (searchInput && searchResults) {
    let pages = [];
    loadSearchData().then(function (data) {
      pages = data;
    });

    searchInput.addEventListener("input", function (e) {
      const query = e.target.value.toLowerCase().trim();

      if (query.length < 2) {
        searchResults.innerHTML = "";
        return;
      }

      const results = pages.filter(function (page) {
        return page.title && page.title.toLowerCase().includes(query);
      });

      displayResults(results);
    });

    function displayResults(results) {
      if (results.length === 0) {
        searchResults.innerHTML = "<p>No results found</p>";
        return;
      }

      searchResults.innerHTML = results
        .map(function (page) {
          return '<a href="' + escapeHTML(page.url) + '">' + escapeHTML(page.title) + "</a>";
        })
        .join("");
    }
  }

});
