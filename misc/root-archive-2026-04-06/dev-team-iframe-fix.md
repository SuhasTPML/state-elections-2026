# iframe Embed Issue: Script Stripped by CMS

## Problem

The election widget iframes embedded on `prajavani-web.qtstage.io` are not rendering correctly. They load content from the wrong domain and do not auto-size.

## Root Cause

The Quintype CMS strips `<script>` tags from HTML embed blocks. The embed snippet relies on JS to:
1. Set the iframe `src` to the correct GitHub Pages URLs
2. Listen for `postMessage` height events and auto-size the iframes

Since the script is stripped, neither works.

## Evidence

Open `https://prajavani-web.qtstage.io/` in Chrome, open DevTools (F12 → Console), and run:

```js
(() => {
  const iframes = Array.from(document.querySelectorAll('iframe'))
    .filter(f => f.id === 'iframe-map' || f.id === 'iframe-results');

  iframes.forEach(f => {
    console.log('--- iframe#' + f.id + ' ---');
    console.log('Resolved src:', f.src);
    console.log('HTML src attr:', f.getAttribute('src'));
  });

  const parent = iframes[0]?.parentElement;
  console.log('Script tag present in embed container:', parent?.querySelector('script') !== null);
  console.log('Embed container HTML:', parent?.innerHTML);
})();
```

### Expected output (if script had run)
```
Resolved src: https://suhastpml.github.io/state-elections-2026/
HTML src attr: https://suhastpml.github.io/state-elections-2026/
Script tag present in embed container: true
```

### Actual output (script stripped)
```
Resolved src: https://prajavani-web.qtstage.io/
HTML src attr: /
Script tag present in embed container: false
```

The `src` attribute is still `"/"` — unchanged from the original HTML — which proves the JS override never ran.

---

## Fix Required

Add the following listener **once** to the global Quintype page template (header or footer JS). This does not need to be in every embed — it just needs to exist somewhere on the page that cannot be stripped.

```js
window.addEventListener('message', function(e) {
  if (!e.data || e.data.type !== 'parliament-embed-size') return;
  var iframes = document.querySelectorAll('iframe');
  for (var i = 0; i < iframes.length; i++) {
    try {
      if (iframes[i].contentWindow === e.source) {
        iframes[i].style.height = e.data.height + 'px';
        break;
      }
    } catch(_) {}
  }
});
```

This listens for height messages broadcast by the embedded widgets and resizes the corresponding iframe automatically. It is safe to add globally — it only acts when a message with `type: 'parliament-embed-size'` is received, and has no effect on any other page or embed.

---

## How the widgets send height

Both `index.html` (map) and `parliament-widget.html` (results) broadcast their rendered height via:

```js
parent.postMessage({ type: 'parliament-embed-size', height: <px>, width: <px>, reason: '...' }, '*');
```

This fires on page load, window resize, and whenever the content repaints (e.g. user switches state or party/alliance view). The parent page listener above catches these and sets `iframe.style.height` accordingly.
