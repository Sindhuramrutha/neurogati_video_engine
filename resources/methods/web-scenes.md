# Web scenes: scene.html with GSAP, D3, three.js or anime.js

Renderer `web`. The entry file is `scene.html`. Headless Chromium records it
frame by frame, so **time is driven by the recorder, not by the clock**:

- Every animation goes on a GSAP timeline handed to `kit.timeline(tl)` (anime.js:
  an `anime.timeline({autoplay:false})` also works), or is drawn from `t` in a
  function handed to `kit.onSeek(t => ...)` (three.js, canvas).
- Never `setTimeout`, `setInterval`, `requestAnimationFrame` loops, CSS
  transitions or CSS animations for motion: the recorder does not wait for them.
- Call `kit.ready()` once everything is built.

Only these load (the page is offline; nothing else is reachable):

| src | what |
| --- | --- |
| `/kit/webkit.js` | the kit (always) |
| `/lib/gsap.js` | GSAP 3; plugins `/lib/gsap/MotionPathPlugin.js`, `MorphSVGPlugin.js`, `DrawSVGPlugin.js`, `SplitText.js`, `TextPlugin.js`, `Flip.js`, `CustomEase.js` |
| `/lib/d3.js` | D3 7 (scales, shapes, layouts; animate its SVG with GSAP) |
| `/lib/anime.js` | anime.js 3 |
| `/lib/three.js` | three.js as an ES module (`<script type="module">`) |
| `/picture?path=...` | only through `kit.picture(path)` with a path from `kit.pictures` |
| `assets/...` | files you wrote into the scene's own folder |

The kit:

- `Kit.load()` -> `kit` (the brief: `kit.brief`, `kit.look`, `kit.seconds`,
  `kit.width`, `kit.height`, `kit.pictures`)
- `kit.when("exact words")` -> the second they are spoken
- `kit.label(text, {x, y, size, bold, color, background})` -> a centred, measured,
  in-frame label (size is px, at least 36)
- `kit.picture(path, {x, y, height})` -> a slide picture, centred on (x, y)
- `kit.svg()` -> a full-frame SVG for shapes, arrows, D3
- `kit.timeline(tl)`, `kit.onSeek(fn)`, `kit.ready()`

Coordinates are pixels of a 1920x1080 frame; keep things 100 px from the edges.
Position with the kit's options or GSAP (`x`, `y`, `scale`) -- the kit centres with
GSAP's `xPercent/yPercent`, so moving a label never makes it jump.

## Worked example: a picture as the anchor, a flow drawn as it is said

```html
<!doctype html>
<html><head><meta charset="utf-8"></head>
<body>
<script src="/lib/gsap.js"></script>
<script src="/lib/gsap/MotionPathPlugin.js"></script>
<script src="/kit/webkit.js"></script>
<script>
gsap.registerPlugin(MotionPathPlugin);
Kit.load().then(kit => {
  const tl = gsap.timeline();
  const pic = kit.picture(kit.pictures[0], { x: 620, y: 560, height: 620 });
  const title = kit.label("Padma's story", { x: 960, y: 120, size: 64, bold: true });
  const before = kit.label("A promising start", { x: 1450, y: 380, background: kit.look.panel });
  const after = kit.label("The turn", { x: 1450, y: 760, background: kit.look.panel });

  const svg = kit.svg();
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", "M1450 430 L1450 710");
  path.setAttribute("stroke", kit.look.accent);
  path.setAttribute("stroke-width", 8);
  path.setAttribute("fill", "none");
  svg.appendChild(path);
  const length = path.getTotalLength();
  gsap.set(path, { strokeDasharray: length, strokeDashoffset: length });
  const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  dot.setAttribute("r", 14);
  dot.setAttribute("fill", kit.look.accent);
  svg.appendChild(dot);

  tl.from(title, { y: -60, opacity: 0, duration: 0.8 }, 0);
  tl.from(pic, { scale: 0.6, opacity: 0, duration: 1.0 }, 0.4);                   // grows in
  tl.from(before, { x: 200, opacity: 0, duration: 0.8 }, kit.when("promising"));   // on the word
  tl.to(path, { strokeDashoffset: 0, duration: 1.2 }, kit.when("then"));            // drawn
  tl.to(dot, { motionPath: { path, align: path }, duration: 1.6 }, "<0.2");         // travels
  tl.from(after, { y: 120, opacity: 0, duration: 0.8 }, ">-0.2");
  tl.to(pic, { scale: 1.25, x: 80, duration: 1.4 }, kit.when("her body"));          // zoom in
  tl.to(before, { scale: 0.85, opacity: 0.6, duration: 0.8 }, "<");                 // recedes
  kit.timeline(tl);
  kit.ready();
});
</script>
</body></html>
```
