# Self-Critique & QA Report

**Project:** Nishkarsh Khandelwal — "Noise → Signal" portfolio
**Live:** https://my-portfolio-eight-pied-84.vercel.app
**Status:** Deployed to Vercel (Hobby), public.

This document closes out the final two phases of the build: **(7) deployment package** and **(8) self-critique & verification.**

---

## 1. Verification — what was tested and passed

**Static / code**
- JavaScript module parses clean (`node --check`) — no syntax errors.
- Brace/paren/bracket balance verified across all edits.
- JSON-LD `Person` block parses as valid JSON.
- `vercel.json` parses as valid JSON; `sitemap.xml` is well-formed XML.
- Every `getElementById` / query target resolves to a real DOM node.
- All six project links resolve to the correct destinations (JioPulse, SecondPlate, Construct Intelligence → Vercel app, Vision → Drive, ScreenSense, EIEF → repo).

**Live**
- Homepage returns the full rendered HTML and is **publicly reachable** (not behind Vercel Authentication) — confirmed by fetching the production URL.
- `robots.txt`, `sitemap.xml`, and `og.png` are served as static files from the site root by Vercel.

**Accessibility**
- Exactly one `<h1>`; logical heading order through sections.
- Decorative WebGL canvas is `aria-hidden`; all content is real, selectable HTML.
- Skip link present; `:focus-visible` outlines added for keyboard users (important, since the custom cursor hides the default one).
- Full `prefers-reduced-motion` path: static particle field, instant reveals, native scrolling, no idle animation.
- The corner guide menu is keyboard-operable and closes on `Esc`.

**Resilience**
- If a CDN or WebGL fails, a failsafe still reveals all content and hides the loader — the page never ends up blank.

---

## 2. Awwwards-jury self-critique

| Criterion | Read | Notes |
|---|---|---|
| **Concept / originality** | Strong | The site *is* the thesis — noise resolving into signal. Not a template; tied to real work. |
| **Craft / execution** | Strong | Custom GLSL particle field, per-chapter palette + coherence, magnetic cursor, creative loader. |
| **Interactivity** | Strong | Real Memoji guide with cursor-tracking eyes, a click-menu that jumps chapters, an auto-**Tour**, hover-card link previews, hover-zoom chapter dial. |
| **Content / storytelling** | Good | Copy is intelligent and human; the one lever left is per-project depth. |
| **Performance** | Unmeasured | Text-first LCP should be fine; Three.js from CDN is the main weight. Needs a live Lighthouse run. |

**Verdict:** concept + craft + interactivity are genuinely submission-grade and unmistakably personal. The gap to a real award win is depth (case studies) and measured performance — both listed below.

---

## 3. Known limitations / honest risks

- **Projects link out** — there are no in-site case-study pages yet. This is the single biggest lever for an Awwwards submission.
- **Memoji pupil placement** was estimated without a live render; verify on device and nudge if slightly off.
- **Three.js is loaded from a CDN** (~large). Fine for LCP (text-first) but measure Core Web Vitals; consider self-hosting/preloading if needed.
- **Canonical/OG point to the `vercel.app` URL.** When a custom domain is added, re-point them (and `sitemap.xml` / `robots.txt`), then redeploy.
- No automated tests or analytics wired yet (Vercel Web Analytics is one click).

---

## 4. Cross-browser / device notes

- Targets modern evergreen browsers (Chrome, Safari, Edge, Firefox): ES modules, WebGL, `backdrop-filter`, CSS custom properties.
- Mobile: particle count scales down, the left rail is hidden, the avatar shrinks; touch disables the custom cursor and hover-cards (by design).
- Where `backdrop-filter` is unsupported, panels stay readable (solid-enough backgrounds) — graceful, not broken.

---

## 5. Roadmap to push toward an award (optional, not blocking)

1. **Per-project case-study views** — process, visuals, outcomes. Biggest impact.
2. **Run Lighthouse on the live URL**; optimize from real numbers (preload/self-host Three.js if LCP/TBT need it).
3. **Custom domain** → re-point canonical/OG/sitemap → redeploy.
4. Optional flourish: a subtle ambient sound layer with a mute control; a treated cinematic portrait.

---

## 6. Deployment package (phase 7) — contents

| File | Purpose |
|---|---|
| `index.html` | The entire experience (markup, styles, WebGL, interactions). |
| `avatar.js` | Your Memoji, embedded as a base64 data URI (background removed). |
| `og.png` | 1200×630 social-share card. |
| `vercel.json` | Security headers (CSP, HSTS, nosniff, frame/referrer/permissions) + asset caching. |
| `robots.txt` | Allow-all + sitemap reference. |
| `sitemap.xml` | Single-URL sitemap. |
| `.vercelignore` | Keeps source screenshots and the unused `portrait.js` out of the deploy. |
| `README.md` | Overview, structure, run + deploy guide, "before you ship" checklist. |

**Deploy / redeploy:** from the project folder, `vercel --prod`.
