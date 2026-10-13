/**
 * webkit.js -- a web page as a scene program, timed to the narration.
 *
 * A scene page (scene.html) loads this and any of the local libraries:
 *
 *   <script src="/lib/gsap.js"></script>            GSAP (+ /lib/gsap/MotionPathPlugin.js,
 *                                                    MorphSVGPlugin, DrawSVGPlugin, SplitText,
 *                                                    TextPlugin)
 *   <script src="/lib/d3.js"></script>              D3 (SVG drawing, scales, layouts)
 *   <script src="/lib/anime.js"></script>           anime.js 3
 *   <script type="module"> import * as THREE from "/lib/three.js" </script>
 *   <script src="/kit/webkit.js"></script>
 *   <script>
 *     Kit.load().then(kit => {
 *       const title = kit.label("Body image", { x: 960, y: 140, size: 64, bold: true });
 *       const tl = gsap.timeline();
 *       tl.from(title, { y: -40, opacity: 0, duration: 0.8 }, 0);
 *       tl.to(title, { scale: 0.8, y: 90 }, kit.when("sensors"));   // on the spoken word
 *       kit.timeline(tl);       // the recorder seeks it, frame by frame
 *       kit.ready();
 *     });
 *   </script>
 *
 * Time is not real time: the recorder calls `seek(t)` for every frame, so every
 * animation must be a GSAP (or anime.js) timeline handed to `kit.timeline`, or
 * drawn from `t` in a function handed to `kit.onSeek` (three.js, canvas). Never
 * use setTimeout, requestAnimationFrame loops or CSS transitions for motion.
 *
 * What it does for the checks: every visible piece of text (however it was made)
 * is measured at the sampled moments -- box, size, colour, what is behind it --
 * and the kinds of motion in the timelines are listed, so a scene that only
 * fades things in and out can be told from one that explains by motion.
 * `kit.label` and `kit.picture` keep what they make inside the frame's margin.
 */
(function () {
  const MARGIN = 0.05;
  const APPEAR_PROPS = new Set(["opacity", "autoAlpha", "visibility", "display"]);
  const META = new Set(["duration", "delay", "ease", "stagger", "repeat", "yoyo", "repeatDelay",
    "onStart", "onUpdate", "onComplete", "immediateRender", "overwrite", "id", "paused",
    "callbackScope", "data", "inherit", "lazy", "runBackwards", "startAt", "keyframes"]);

  // Centred on its point. With GSAP present, through GSAP's own xPercent/yPercent:
  // a CSS translate would be replaced by the first GSAP move, and the element jump.
  const centre = el => {
    if (window.gsap) window.gsap.set(el, { xPercent: -50, yPercent: -50 });
    else el.style.transform = "translate(-50%, -50%)";
  };

  const words = text => (String(text).toLowerCase().match(/[a-z0-9']+/g) || []);

  const hex = colour => {
    const m = String(colour).match(/rgba?\(([^)]+)\)/);
    if (!m) return colour;
    const [r, g, b, a = 1] = m[1].split(",").map(Number);
    if (a === 0) return null;
    return "#" + [r, g, b].map(v => Math.round(v).toString(16).padStart(2, "0")).join("");
  };

  class Kit {
    static async load() {
      const brief = await (await fetch("/brief.json")).json();
      window.__kit = new Kit(brief);
      return window.__kit;
    }

    constructor(brief) {
      this.brief = brief;
      this.look = brief.look || {};
      this.seconds = brief.seconds;
      this.width = brief.width;
      this.height = brief.height;
      this.pictures = (brief.assets && brief.assets.pictures) || [];
      this._timelines = [];
      this._seekers = [];
      this._spoken = [];
      (brief.words || []).forEach((w, i) => words(w.text).forEach(part =>
        this._spoken.push([i, part])));
      const body = document.body;
      Object.assign(document.documentElement.style, { margin: 0, padding: 0 });
      Object.assign(body.style, {
        margin: 0, width: `${this.width}px`, height: `${this.height}px`, overflow: "hidden",
        position: "relative", background: this.look.background || "#0d0f14",
        color: this.look.text || "#e8eaf0",
        fontFamily: `${this.look.body_font || "Segoe UI"}, Arial, sans-serif`,
      });
      this.stage = document.getElementById("stage") || body;
    }

    /** The second these words start being spoken. */
    when(phrase, fallback) {
      const wanted = words(phrase);
      const flat = this._spoken;
      for (let s = 0; s + wanted.length <= flat.length; s++) {
        if (wanted.every((w, k) => flat[s + k][1] === w)) {
          return this.brief.words[flat[s][0]].start_ms / 1000;
        }
      }
      if (fallback !== undefined) return fallback;
      const said = words(this.brief.narration || "");
      for (let s = 0; s + wanted.length <= said.length; s++) {
        if (wanted.every((w, k) => said[s + k] === w)) return this.seconds * s / Math.max(1, said.length);
      }
      return 0;
    }

    /** Words on screen, centred on (x, y) in pixels, kept inside the margin. */
    label(text, options = {}) {
      const { x = this.width / 2, y = this.height / 2, size = 44, color, bold = false,
        parent = this.stage, background } = options;
      const el = document.createElement("div");
      el.className = "kit-label";
      el.textContent = text;
      Object.assign(el.style, {
        position: "absolute", left: `${x}px`, top: `${y}px`,
        fontSize: `${Math.max(36, size)}px`, fontWeight: bold ? 700 : 400, whiteSpace: "nowrap",
        color: color || this.look.text, lineHeight: 1.15,
        ...(background ? { background, padding: "8px 16px", borderRadius: "10px" } : {}),
      });
      parent.appendChild(el);
      centre(el);
      this.fit(el);
      return el;
    }

    /** A picture from brief.assets.pictures, `height` pixels tall at (x, y). */
    picture(path, options = {}) {
      const { x = this.width / 2, y = this.height / 2, height = 500, parent = this.stage } = options;
      const img = document.createElement("img");
      img.src = `/picture?path=${encodeURIComponent(path)}`;
      Object.assign(img.style, { position: "absolute", left: `${x}px`, top: `${y}px`,
        height: `${height}px` });
      parent.appendChild(img);
      centre(img);
      return img;
    }

    /** An SVG covering the frame, for D3 or hand-drawn shapes. */
    svg(parent = this.stage) {
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("width", this.width);
      svg.setAttribute("height", this.height);
      svg.setAttribute("viewBox", `0 0 ${this.width} ${this.height}`);
      Object.assign(svg.style, { position: "absolute", left: 0, top: 0 });
      parent.appendChild(svg);
      return svg;
    }

    /** Move (and if need be shrink) an element so it sits inside the margin. */
    fit(el) {
      const r = el.getBoundingClientRect();
      const left = this.width * MARGIN, right = this.width * (1 - MARGIN);
      const top = this.height * MARGIN, bottom = this.height * (1 - MARGIN);
      if (r.width > right - left) el.style.fontSize = `${parseFloat(el.style.fontSize || 44) * (right - left) / r.width * 0.98}px`;
      const s = el.getBoundingClientRect();
      const dx = Math.max(0, left - s.left) - Math.max(0, s.right - right);
      const dy = Math.max(0, top - s.top) - Math.max(0, s.bottom - bottom);
      if (dx || dy) {
        el.style.left = `${parseFloat(el.style.left) + dx}px`;
        el.style.top = `${parseFloat(el.style.top) + dy}px`;
      }
      return el;
    }

    timeline(tl) { tl.pause(0); this._timelines.push(tl); return tl; }
    onSeek(fn) { this._seekers.push(fn); }
    ready() { this.seek(0); window.__kitReady = true; }

    seek(t) {
      for (const tl of this._timelines) {
        if (typeof tl.seek === "function") tl.seek(Math.min(t, tl.duration ? tl.duration() : t), false);
      }
      for (const fn of this._seekers) fn(t);
    }

    /** The kinds of motion in the timelines: appear-only, or explaining. */
    motions() {
      if (!this._timelines.length) return null;
      const plays = [];
      for (const tl of this._timelines) {
        if (!tl.getChildren) { plays.push(["Move"]); continue; }
        for (const tween of tl.getChildren(true, true, false)) {
          const props = Object.keys(tween.vars || {}).filter(k => !META.has(k));
          plays.push([props.length && props.every(p => APPEAR_PROPS.has(p)) ? "FadeIn" : "Move"]);
        }
      }
      return plays;
    }

    /** Everything on screen now, for the checks. */
    snapshot(t) {
      const visible = el => {
        let alpha = 1;
        for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
          const s = getComputedStyle(n);
          if (s.display === "none" || s.visibility === "hidden") return 0;
          alpha *= parseFloat(s.opacity);
        }
        return alpha;
      };
      const behind = el => {
        for (let n = el.parentElement; n; n = n.parentElement) {
          const c = hex(getComputedStyle(n).backgroundColor);
          if (c) return c;
        }
        return this.look.background;
      };
      const texts = [];
      for (const el of document.body.querySelectorAll("*")) {
        if (["SCRIPT", "STYLE"].includes(el.tagName)) continue;
        const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join("").trim();
        if (!own || visible(el) < 0.5) continue;
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        const s = getComputedStyle(el);
        texts.push({ text: own, box: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)],
          line_height: Math.round(parseFloat(s.fontSize)), color: hex(s.color) || this.look.text,
          behind: hex(s.backgroundColor) || behind(el) });
      }
      const shapes = document.body.querySelectorAll("path, circle, rect, line, polyline, polygon, ellipse, img, canvas");
      let graphics = 0;
      const pictures = [];
      for (const el of shapes) {
        if (visible(el) < 0.3) continue;
        const r = el.getBoundingClientRect();
        if (!r.width && !r.height) continue;
        graphics += 1;
        if (el.tagName === "IMG" && el.src.includes("/picture?")) {
          pictures.push([Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]);
        }
      }
      // Where a drawn outline (an SVG path, line, circle, rect) runs through words,
      // followed at most 6 px between samples: 32 fixed samples left gaps on a long
      // line wide enough for a whole line of words to fall between.
      const crossings = [];
      const closed = [];
      const open = [];
      const W = innerWidth, H = innerHeight;
      const geometry = document.body.querySelectorAll("path, line, polyline, polygon, circle, ellipse, rect");
      for (const shape of geometry) {
        if (visible(shape) < 0.3 || typeof shape.getTotalLength !== "function") continue;
        const style = getComputedStyle(shape);
        if (!style.stroke || style.stroke === "none" || !(parseFloat(style.strokeWidth) > 0)) continue;
        const matrix = shape.getScreenCTM();
        const length = shape.getTotalLength();
        if (!matrix || !length) continue;
        const count = Math.min(800, Math.max(32, Math.ceil(length * Math.hypot(matrix.a, matrix.b) / 6)));
        const points = [];
        for (let step = 0; step <= count; step++) {
          const p = shape.getPointAtLength(length * step / count);
          points.push([p.x * matrix.a + p.y * matrix.c + matrix.e, p.x * matrix.b + p.y * matrix.d + matrix.f]);
        }
        for (const piece of texts) {
          const [x0, y0, x1, y1] = piece.box;
          if (points.some(([x, y]) => x0 + 4 < x && x < x1 - 4 && y0 + 4 < y && y < y1 - 4)) {
            crossings.push({ text: piece.text.slice(0, 40), shape: shape.tagName });
          }
        }
        const r = shape.getBoundingClientRect();
        const isClosed = ["circle", "ellipse", "rect", "polygon"].includes(shape.tagName)
          || (shape.tagName === "path" && /z\s*$/i.test(shape.getAttribute("d") || ""));
        if (!isClosed) open.push({ points, name: shape.tagName });
        if (isClosed && r.width >= 40 && r.height >= 40 && !(r.width >= 0.9 * W && r.height >= 0.9 * H)) {
          const words = texts.find(({ box: [a, b, c, d] }) => r.left < (a + c) / 2 && (a + c) / 2 < r.right
            && r.top < (b + d) / 2 && (b + d) / 2 < r.bottom);
          closed.push({ points, name: shape.tagName + (words ? ` around “${words.text.slice(0, 30)}”` : "") });
        }
      }
      // Closed outlines (boxes, circles) that run through each other: part of one
      // well inside the other and part well outside. Nested or touching is fine.
      const inside = ([x, y], poly) => {
        let odd = false;
        for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
          const [xi, yi] = poly[i], [xj, yj] = poly[j];
          if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) odd = !odd;
        }
        return odd;
      };
      const clear = (p, poly) => poly.every(([x, y]) => Math.hypot(x - p[0], y - p[1]) > 4);
      const runsThrough = (a, b) => {
        let inner = false, outer = false;
        for (const p of a) {
          if (!clear(p, b)) continue;
          if (inside(p, b)) inner = true; else outer = true;
          if (inner && outer) return true;
        }
        return false;
      };
      const collisions = [];
      for (let i = 0; i < closed.length; i++) {
        for (let j = i + 1; j < closed.length; j++) {
          if (runsThrough(closed[i].points, closed[j].points) || runsThrough(closed[j].points, closed[i].points)) {
            collisions.push({ a: closed[i].name, b: closed[j].name });
          }
        }
      }
      // A line or arrow that goes into a box and out again -- or ends inside it --
      // runs over what the box holds; one that stops at the edge is clear of it.
      for (const line of open) {
        for (const box of closed) {
          if (runsThrough(line.points, box.points)) collisions.push({ a: line.name, b: box.name });
        }
      }
      // How much of the frame is used: everything drawn, but a full-frame background.
      const boxes = texts.map(p => p.box).concat(pictures);
      for (const el of shapes) {
        if (visible(el) < 0.3) continue;
        const r = el.getBoundingClientRect();
        if ((!r.width && !r.height) || (r.width >= 0.9 * W && r.height >= 0.9 * H)) continue;
        boxes.push([r.left, r.top, r.right, r.bottom]);
      }
      const extent = boxes.length ? [0, 1, 2, 3].map(k => Math.round((k < 2 ? Math.min : Math.max)(...boxes.map(b => b[k])))) : null;
      return { at: Math.round(t * 100) / 100, texts, graphics: Math.min(graphics, 50), pictures, crossings,
        collisions, extent };
    }
  }

  window.Kit = Kit;
})();
