# ETRI newsletter design QA

- Source of truth: `C:\Users\JEON\Documents\홍보물제작\KISTpromotion-pages\kist-connect-2026.png`
- Implementation: `C:\Users\JEON\Documents\기술판매\ETRI\newsletter\etri-medical-ai-newsletter.html`
- Desktop screenshot: `C:\Users\JEON\Documents\기술판매\tmp\etri-newsletter\desktop.png`
- Mobile screenshot: `C:\Users\JEON\Documents\기술판매\tmp\etri-newsletter\mobile.png`
- Combined comparison: `C:\Users\JEON\Documents\기술판매\tmp\etri-newsletter\kist-reference-vs-etri.png`

## Verification

- Desktop viewport: 900 x 1000 px; newsletter rendered at 600 px.
- Mobile viewport: 360 x 800 px; newsletter rendered at 360 px.
- Reference comparison width: 600 px.
- Implementation comparison width: 600 px.
- Full-page desktop and mobile captures reviewed.
- Hero, two-column technology cards, CTA/contact block, and footer reviewed as focused regions.

## Findings and fixes

- Matched the KIST reference hierarchy: dark navy field, oversized cyan headline, right-side technical hero image, two-column folder cards, cyan CTA accents, and compact footer.
- Replaced the original one-column white cards with four 280 x 190 px linked raster cards.
- Kept each technology card as an individual link instead of using an image map.
- Preserved the 600 px table-based email structure and absolute GitHub Pages asset URLs.
- Found contact text overlap in the 360 px render; changed the contact block to a centered stacked layout.
- Final render: zero horizontal overflow, zero console errors, and zero failed image requests.

## History

1. Initial KIST-style implementation completed and rendered.
2. Mobile contact overlap found during visual review.
3. Contact block stacked and re-rendered.
4. Desktop and mobile validation passed.

## Final result

passed
