---
title: Formulieren Stylen
last_modified: 2026-11-18 11:58:43 +0100
created: 2025-04-24 16:25:02 +0200
---

# HTML

```html 
<form action="/submit" method="post">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required><br>

  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required><br>

  <label for="message">Message:</label>
  <textarea id="message" name="message" required></textarea><br>

  <button type="submit">Submit</button>
</form>
```

# CSS 

## Basic styling 

{% include browser.html img='images/form style 1.png' %}

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

## Focus 

{% include browser.html img='images/form style field bolder.gif' %}

```css
input:focus,
textarea:focus {
  border: 2px solid darkcyan;
}
```

# Extra info

Extra informatie over het stylen van forms kan je vinden op:

- [W3Schools](https://www.w3schools.com/css/css_form.asp)
- [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Styling_web_forms)
