---
title: Formulieren Stylen
last_modified: 2025-04-24 16:34:32 +0200
created: 2025-04-24 16:25:02 +0200
---

# Voorbeelden

```css
label {
  /* rechtse uitlijning van de labels */
  display: inline-block;
  width: 90px;
  text-align: right;
}

textarea {
  vertical-align: top; /* plaats het label bovenaan */
  height: 40px;
  width: 195px;
}
```

{% include browser.html img='images/form style 1.png' %}

```css
input:focus,
textarea:focus {
  border: 2px solid darkcyan;
}
```

{% include browser.html img='images/form style field bolder.gif' %}

# Extra info

Extra informatie over het stylen van forms kan je vinden op:

- [W3Schools](https://www.w3schools.com/css/css_form.asp)
- [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Styling_web_forms)
