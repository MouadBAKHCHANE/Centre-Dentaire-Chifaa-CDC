# SEO · GEO · Speed audit — Centre Dentaire Chifaa (Meknès)

**Date:** 2026-10-01  
**Scope:** full site, all 18 indexable URLs, plus the 2 legal pages (noindex).  
**Live URL:** https://www.centredentairechifaa.ma/ (the bare domain answers with a 308 redirect to `www`).  
**Evidence:**
- built HTML of every page, parsed locally
- live HTTP headers
- robots.txt, sitemap.xml and llms.txt fetched from the live site
- one Lighthouse 12 mobile run on the live home page (lab data)
- the earlier plan in [ACTION-PLAN-SEO-MEKNES.md](ACTION-PLAN-SEO-MEKNES.md)

## A) Summary

**Overall: Good foundation (~70/100). Score confidence: medium**, because there is no field data and no Search Console access.

The previous plan's on-page work is mostly done:
- 6 specialty pages with "spécialité + Meknès" slugs, H1s and titles
- Dentist, MedicalProcedure, BlogPosting and BreadcrumbList schema
- sitemap, `lang="fr"`, canonicals, Open Graph
- 6 blog articles

The remaining gaps are technical polish, speed on mobile, and E-E-A-T and GEO signals around the doctor.

| Category | Rating | Driver |
|---|---|---|
| Technical SEO | Good (~75) | Solid base; home canonical missing; robots.txt points to the wrong host; no cache or security headers |
| On-page | Good (~70) | Keyword-led titles and H1s; many titles are 70–103 characters long; three weak H1s |
| Schema | Good (~70) | Rich graph; the home `Dentist` entity has no `@id` that other pages link to, and no Person for the doctor |
| Content / E-E-A-T | Needs work (~55) | Health topic (YMYL), yet the articles have no author byline or visible date and never name the doctor |
| Performance (mobile lab) | Needs work (70) | LCP 4.5 s, FCP 3.0 s, TBT 240 ms, CLS 0 |
| Images | Needs work (~60) | Oversized logo and avatars; no WebP/AVIF; no `srcset` |
| GEO (AI search) | Needs work (~50) | No llms.txt; AI crawlers allowed only by default; few short, quotable answers |

**Top 3 issues**
1. The doctor is almost invisible to search engines and AI assistants. Blog articles are signed by an Organization, with no byline or date, there is no doctor page, and there is no Person schema.
2. Mobile LCP is 4.5 s. Google Fonts block rendering for about 0.9 s, the hero poster isn't preloaded, and every file is served with `Cache-Control: max-age=0`.
3. Several identity details are inconsistent:
   - the home page has no canonical
   - the home page's `og:image` is relative
   - robots.txt names `centredentairechifaa.ma`, while the sitemap and canonicals use `www`
   - the home `Dentist` entity has no `@id`, so the `…/#cabinet` references on the other pages point to nothing

**Top 3 opportunities**
1. A page for Dr Taoufik Boukadous with Person schema, linked as the author or reviewer of every article. This is the strongest E-E-A-T and GEO lever for a dental clinic.
2. An emergency page (`/urgence-dentaire-meknes/`), a high-intent query with little local competition (see the earlier plan).
3. Moving the "Performance" score from 70 to above 90 with a small set of fixes: cache headers, fonts, poster preload and image weights.

## B) Findings

| # | Area | Severity | Confidence | Finding | Evidence | Fix |
|---|---|---|---|---|---|---|
| 1 | Technical | Warning | Confirmed | Home page has no canonical | `index.html` has no `<link rel="canonical">`; the other 19 pages have one | Add `<link rel="canonical" href="https://www.centredentairechifaa.ma/">` |
| 2 | Technical | Warning | Confirmed | robots.txt points to a non-canonical sitemap host and still has a "replace domain" comment | `Sitemap: https://centredentairechifaa.ma/sitemap.xml`; the sitemap `<loc>` values use `www` | Point it to `https://www.centredentairechifaa.ma/sitemap.xml` and drop the comment |
| 3 | Technical | Info | Confirmed | Sitemap has no `<lastmod>` | 18 URLs, no lastmod | Have the generator write the build date (or the page's date) |
| 4 | Technical / Speed | Warning | Confirmed | No browser caching on static files | `Cache-Control: public, max-age=0, must-revalidate` on CSS, JS, JPG and MP4 | Add a `vercel.json` with headers: `immutable, max-age=31536000` for `/vendor/*` and the versioned `dark.css`/`dark.js`; `max-age=2592000` for `/assets/*` |
| 5 | Technical | Info | Confirmed | 5 security headers missing | security_headers.py: no CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy or Permissions-Policy; HSTS has no includeSubDomains | Add them in the same `vercel.json` (CSP needs testing because of the Google Fonts, Maps and wa.me links) |
| 6 | Speed | Warning | Confirmed | Render-blocking Google Fonts | Lighthouse: fonts.googleapis.com costs about 896 ms, dark.css about 365 ms | Self-host Geist and Geist Mono (woff2, `font-display: swap`, preload the 400 weight), or at least add `preconnect` |
| 7 | Speed | Warning | Confirmed | LCP is the hero video poster, found late | LCP element is `<video … poster="assets/img/hero-poster.jpg">`, 4.5 s | `<link rel="preload" as="image" href="/assets/img/hero-poster.jpg" fetchpriority="high">`; serve the poster as WebP |
| 8 | Images | Warning | Confirmed | Logo is a 1156×479 PNG (158 KB) shown at 132×55 | Lighthouse uses-responsive-images: 147 KB wasted | Export at 264×110 in WebP/PNG (about 8–12 KB), in both light and dark versions |
| 9 | Images | Warning | Confirmed | Review avatars are 240 px files of 47–96 KB, shown at about 40 px | `av-g1/2/3.jpg` | Resize to 96 px WebP (about 3 KB each) |
| 10 | Images | Warning | Confirmed | No modern formats or responsive sizes | Lighthouse: modern-image-formats saves 518 KB, responsive images 507 KB | Generate WebP copies and a `srcset` in the build script (`<picture>`) |
| 11 | Images | Info | Confirmed | Most `<img>` tags have no width/height | e.g. 14/16 on home, 20/22 on /blog/ | CLS is already 0 thanks to CSS aspect-ratios, so this is maintenance only |
| 12 | On-page | Warning | Confirmed | Titles too long (cut off in results) | Blog titles are 82–103 characters, soins pages 70–82 | Keep ≤ 60 characters; use the suffix "· CDC Meknès" instead of "\| Centre Dentaire Chifaa, Meknès" |
| 13 | On-page | Warning | Confirmed | Meta descriptions too long on the soins pages | 186–200 characters | Keep ≤ 155 characters |
| 14 | On-page | Warning | Confirmed | Weak or odd H1s | /contact/ "Contact", /equipements/ "Équipements", /blog/ "Blog dentaire du Centre Dentaire Chifaa : Blog" | Keep the giant word on screen, but put a full H1 in the markup, e.g. "Contact — dentiste à Meknès, Av des FAR" (the visible word can be a styled span) |
| 15 | On-page / compliance | Warning | Hypothesis | Home H1 claims "Votre **meilleur** dentiste à Meknès" | `<h1>` on index.html | Superlatives in medical advertising may breach the Moroccan dental code of ethics; ask the doctor. The earlier plan's wording: "Votre dentiste à Meknès, …" |
| 16 | Schema | Warning | Confirmed | Home `Dentist` entity has no `@id`, `url`, `logo` or `image`, and has an empty `email` | JSON-LD on index.html; other pages point to `…/#cabinet` | Add `"@id": "https://www.centredentairechifaa.ma/#cabinet"`, `url`, `logo`, `image`, `medicalSpecialty`; remove `"email": ""` until the real e-mail is known |
| 17 | Schema / E-E-A-T | Warning | Confirmed | No Person entity for the dentist | No `Person`; BlogPosting `author` is `Organization` | Add `Person` (Dr Taoufik Boukadous, `jobTitle`, `worksFor` #cabinet, `alumniOf`/`hasCredential` once known); use it as `author` or `reviewedBy` |
| 18 | Schema | Info | Confirmed | `aggregateRating` 5.0 / 43 is hard-coded | Home JSON-LD | Google doesn't show stars for self-published LocalBusiness ratings; keep only if updated regularly, otherwise remove |
| 19 | Schema | Info | Confirmed | FAQPage on /contact/ | Contact JSON-LD | Valid, but FAQ rich results are limited to health and government authorities; harmless, so keep for GEO |
| 20 | Content / E-E-A-T | Warning | Confirmed | Articles have no author byline, no visible date and never name the doctor | Blog implant article: 0 mentions of "Boukadous", date only in JSON-LD | Show "Rédigé par Dr Taoufik Boukadous, chirurgien-dentiste · mis à jour le …" with a link to the doctor page |
| 21 | Content | Warning | Confirmed | Articles are short for health content | 607–784 words | Expand the strongest ones to 1,000+ words: an FAQ block, when to consult, a link to the matching soin page |
| 22 | Content | Warning | Confirmed | Planned emergency and doctor pages don't exist | Sitemap: no `/urgence…/`, no `/dr-…/` | Create both (see the action plan) |
| 23 | GEO | Warning | Confirmed | No llms.txt | HTTP 404 on /llms.txt | Add a short llms.txt: who, where, specialties, hours, key URLs |
| 24 | GEO | Info | Confirmed | AI crawlers allowed only by default | 11 bots inherit `User-agent: *` | Optional: list GPTBot, ClaudeBot, PerplexityBot, Google-Extended… with `Allow: /` to make the choice explicit |
| 25 | GEO | Warning | Likely | Few short, quotable answers | Soins pages open with marketing H2s ("Remplacer une dent absente, durablement…") | Add a 40–60 word "En bref" answer under each H1 (what it is, for whom, duration, devis), so AI assistants can quote it |
| 26 | Accessibility | Info | Confirmed | 3 Lighthouse accessibility failures (score 93) | `.s-dots role="tablist"` has no `tab` children; heading order skips (h3); the Maps link's `aria-label` doesn't match its visible text | Fix the roles, adjust heading levels, make the aria-label include the visible text |
| 27 | Social | Info | Confirmed | Relative `og:image` on home; no Twitter cards | `content="assets/img/hero-poster.jpg"` | Make it absolute; add `twitter:card=summary_large_image` |
| 28 | Licence | Warning | Confirmed | Caliora template images are publicly served | `/assets/img/About _ Caliora…/…avif` returns 200; the contact hero uses a Caliora image | Replace with the cabinet's photos or free-licence images, then delete the folder |

**Passes:**
- HTTPS with HSTS
- a single redirect hop from the bare domain to `www`
- server response in 40 ms
- one H1 per page
- `lang="fr"`
- every image has an `alt` attribute
- legal pages are noindex, follow
- BreadcrumbList on all inner pages
- CLS of 0
- Lighthouse SEO 100 and Best Practices 100

## C) Prioritised action plan
See [ACTION-PLAN.md](ACTION-PLAN.md).

## D) Unknowns and follow-ups
- **Field data (CrUX) and indexing status are unknown.** The PageSpeed API was rate-limited during the audit and the site is new. Check Google Search Console (Pages, Core Web Vitals) about 4 weeks after the domain is verified.
- **Rankings, traffic and backlinks:** I have no data. Track "dentiste meknes", "implant dentaire meknes", "orthodontiste meknes", "dentiste enfant meknes" and "urgence dentaire meknes" in Search Console.
- **Google Business Profile:** I couldn't check that its NAP (name, address, phone) and website link match the site exactly.
- **Finding 15:** the doctor should confirm what the Ordre allows in advertising wording.
- **Lighthouse:** a single lab run on the home page only. Re-run on /soins/implants-dentaires-meknes/ and /blog/ after the speed fixes.
