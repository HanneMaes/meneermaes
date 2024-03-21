---
title: Webtechnology
layout: default
date: Wed, Mar 20, 2024  3:36:23 PM
---

# Responive

{% capture code %}
    .left, .right {
        float: left;
        width: 20%; /* The width is 20%, by default */
    }

    .main {
        float: left;
        width: 60%; /* The width is 60%, by default */
    }

    /* Use a media query to add a breakpoint at 800px: */
    @media screen and (max-width: 800px) {
        .left, .main, .right {
        width: 100%; /* The width is 100%, when the viewport is 800px or smaller */
        }
    }
{% endcapture %}
{% include code.html title="css" content=code %}

