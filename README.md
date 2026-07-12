# Nishkarsh Khandelwal — Portfolio · "Noise → Signal"

An award-tier personal portfolio built as a single, self-contained WebGL experience. The whole site is a living particle field that resolves from noise into structure as you descend through six chapters — a direct expression of the thesis: *turning messy, real-world data into intelligent systems.*

**Live concept:** Signal → How I Think → The Work → The Question (EIEF) → Foundations → Signal Out.

**Link:** https://my-portfolio-eight-pied-84.vercel.app/

---

## Tech

- **Three.js (r0.160)** — GPU particle field with a custom GLSL shader (simplex-noise turbulence, per-chapter colour + coherence, magnetic-cursor repulsion).
- **GSAP + ScrollTrigger** — scroll choreography, chapter transitions, count-ups, reveal batches.
- **Lenis** — smooth scrolling (disabled under `prefers-reduced-motion`).
- **Vanilla HTML/CSS/JS** — no build step. Fonts: Space Grotesk, JetBrains Mono, Inter (Google Fonts).

Everything loads from CDNs; there is **nothing to compile**.

---

## Project structure

```
My Portfolio/
├── index.html      # the entire experience (markup, styles, WebGL, interactions)
├── avatar.js       # your Memoji, embedded as a base64 data URI (the corner guide)
├── og.png          # 1200×630 social-share image
├── robots.txt
├── sitemap.xml
├── vercel.json     # security headers + caching
└── README.md
```

The interactive corner guide (your Memoji) is a menu: jump to any chapter, launch an auto-scrolling **Tour**, or open GitHub/email. Its eyes track the cursor.

---

## Run locally

It's a static site — just open `index.html` in a modern browser (Chrome, Safari, Edge, Firefox). Keep `avatar.js` and `og.png` in the same folder.

For a local server (recommended, avoids any file:// quirks):

```bash
# from inside the folder
python3 -m http.server 5173
# then visit http://localhost:5173
```

---

## Deploy to Vercel

1. Put this folder in a Git repo (GitHub/GitLab/Bitbucket) and push.
2. On [vercel.com](https://vercel.com) → **New Project** → import the repo.
3. Framework preset: **Other**. Build command: *none*. Output directory: `./` (root). Deploy.

Or with the CLI:

```bash
npm i -g vercel
vercel          # preview
vercel --prod   # production
```

`vercel.json` already sets security headers (CSP, HSTS, nosniff, frame options, referrer + permissions policy) and long-cache for `avatar.js` / `og.png`.

### Custom domain
In Vercel → Project → **Settings → Domains**, add your domain and follow the DNS records shown.

### Analytics (optional)
Enable **Vercel Web Analytics** (Project → Analytics → Enable) — no code needed for the basic version. For privacy-first stats, add a Plausible/Umami script tag in `<head>`.

---

## ⚠️ Before you ship — replace the placeholder domain

The code uses `https://nishkarsh.dev/` as a placeholder. Swap it for your real domain in:

- `index.html` → `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, and the JSON-LD `url`
- `robots.txt` → `Sitemap:` line
- `sitemap.xml` → `<loc>`

Also confirm the project links are correct in `index.html` (JioPulse, SecondPlate, Construct Intelligence, Vision, ScreenSense, and the EIEF repo).

---

## Performance / Accessibility / SEO

- **Performance:** device-pixel-ratio capped at 2; particle count scales down on mobile; render loop pauses when the tab is hidden; fonts use `display=swap`; assets are long-cached.
- **Accessibility:** all content is real HTML (the canvas is `aria-hidden`); logical heading order (single `h1`); skip link; visible `:focus-visible` rings for keyboard users; a full `prefers-reduced-motion` path (static field, instant reveals, native scroll); the corner guide is keyboard-operable and closes on `Esc`.
- **SEO:** title/description, canonical, Open Graph + Twitter cards with a real `og.png`, `robots` directives, `sitemap.xml`, and JSON-LD `Person` structured data.
- **Graceful degradation:** if a CDN or WebGL fails, a failsafe still reveals all content and hides the loader — the site never ends up blank.

---

## Credits

Design, engineering & words: **Nishkarsh Khandelwal**. Built with Three.js, GSAP, and Lenis.
