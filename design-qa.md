# ETRI medical AI newsletter design QA

- Primary reference: `C:\Users\JEON\Desktop\04.png`
- Secondary reference: `C:\Users\JEON\Documents\홍보물제작\KISTpromotion-pages\kist-connect-2026.png`
- Full poster: `C:\Users\JEON\Documents\기술판매\ETRI\newsletter\etri-medical-ai-newsletter-poster.png`
- HTML newsletter: `C:\Users\JEON\Documents\기술판매\ETRI\newsletter\etri-medical-ai-newsletter.html`
- Desktop capture: `C:\Users\JEON\Documents\기술판매\tmp\etri-newsletter\desktop.png`
- Mobile capture: `C:\Users\JEON\Documents\기술판매\tmp\etri-newsletter\mobile.png`
- Three-way comparison: `C:\Users\JEON\Documents\기술판매\tmp\etri-newsletter\reference-comparison.png`

## Reference interpretation

- Build one continuous vertical promotional poster rather than a narrow web landing page.
- Use a large publication-style title, a subject-specific hero visual, dense technology information, repeated CTA treatment, and a clear terminal consultation action.
- Preserve the dark navy and cyan technical visual language shared by both references.
- Avoid the rejected folder motif and avoid inserting separate images inside the four technology panels.

## Implementation

- Master artwork: 1200 x 2860 px.
- Display width: 600 px for 2x raster sharpness.
- Seven seamless linked image slices: hero, four technologies, email CTA, and telephone contact.
- Four technology slices link individually to `tech-01.html` through `tech-04.html`.
- Email and telephone regions use separate clickable image slices.
- All copy is rasterized with Hancom Gothic Bold/Regular and Arial at 2x resolution.
- Old newsletter header, hero, and four card assets removed from the active asset set.

## Verification

- Desktop viewport: 900 x 1000 px.
- Mobile viewport: 360 x 800 px.
- Zero horizontal overflow.
- Zero console errors.
- Zero failed image requests.
- Six automated tests passed.
- Visual comparison confirms consistent vertical-poster hierarchy across both references and the implementation.

## Final result

passed

---

# Catholic SMK researcher-card KIST alignment design QA

- Source visual truth: `C:\Users\JEON\Documents\기술판매\tmp\kist-researcher-reference.png`
- Implementation screenshots:
  - `C:\Users\JEON\Documents\기술판매\tmp\catholic-smk1-researcher-after.png`
  - `C:\Users\JEON\Documents\기술판매\tmp\catholic-smk2-researcher-after.png`
  - `C:\Users\JEON\Documents\기술판매\tmp\catholic-smk3-researcher-after.png`
- Viewport and capture: 1280 x 720 CSS px, 1280 x 720 output px, 1x density.
- State: initial desktop view, no hover or focus state.

## Full-view comparison evidence

- KIST and Catholic pages retain the same two-column A4-landscape SMK composition.
- The researcher card stays aligned to the top-right hero area without overlap or clipping.
- No unrelated layout, color, image, table, or content changes were introduced.

## Focused region comparison evidence

- Typography matches the KIST card: label 22px/800, name 21px/800, position 15px/600, affiliation 14px/500 with 18.2px line height.
- All three Catholic pages use the same three-line content hierarchy: `연구책임자`, `{이름} 교수`, `가톨릭대학교 화학과`.
- The patent title was removed only from the researcher-card affiliation line; IP portfolio content remains unchanged.

## Required fidelity surfaces

- Fonts and typography: KIST sizes and weights matched exactly for all four researcher-card text roles.
- Spacing and layout rhythm: existing card padding, border, right alignment, gaps, and hero grid retained.
- Colors and visual tokens: existing Catholic purple and cool-gray tokens retained.
- Image quality and asset fidelity: no image assets changed.
- Copy and content: names retained; position normalized to `교수`; affiliation normalized to `가톨릭대학교 화학과`.

## Comparison history

- Initial P1: Catholic label and supporting text were smaller than KIST, and the affiliation line contained the patent title.
- Fix: copied KIST font-size hierarchy and replaced position/affiliation copy in all three pages.
- Post-fix evidence: all three browser-rendered cards report 22px, 21px, 15px, and 14px; zero console errors.

## Findings

- No actionable P0, P1, or P2 differences remain in the requested researcher-card scope.

## Final result

passed

---

# ETRI Deadwater-style IP technology list design QA

- Primary reference: `C:\Users\JEON\Documents\기술판매\ETRI\deadwater-newsletter\reference\deadwater.html`
- Design specification: `C:\Users\JEON\Documents\기술판매\ETRI\deadwater-newsletter\reference\deadwater-design.md`
- Implementation: `C:\Users\JEON\Documents\기술판매\ETRI\deadwater-newsletter\index.html`
- Desktop capture: `C:\Users\JEON\Documents\기술판매\tmp\etri-deadwater-newsletter\desktop.png`
- Hover capture: `C:\Users\JEON\Documents\기술판매\tmp\etri-deadwater-newsletter\hover-tech-02.png`
- Mobile capture: `C:\Users\JEON\Documents\기술판매\tmp\etri-deadwater-newsletter\mobile.png`
- Side-by-side comparison: `C:\Users\JEON\Documents\기술판매\tmp\etri-deadwater-newsletter\comparison.png`

## Reference interpretation

- Use the original `deadwater.html` as the implementation skeleton rather than redrawing its composition.
- Retain its embedded fonts, full-width canvas, black editorial field, oversized condensed wordmark, spacing system, fine rules, project list, reveal behavior, custom cursor, and sticky preview.
- Limit the page to the source composition before the Expertise section.
- Remove the showreel DOM and behavior, then connect the original project-preview interaction to SMK captures and direct technology links.

## Verification

- Desktop canvas: unrestricted full viewport width; verified at 1440 px.
- Mobile viewport: zero horizontal overflow at 390 px.
- Four technology links: new-tab targets verified.
- Hover preview: row 02 loads `smk-02.png` and becomes visible.
- Zero video elements, zero Expertise section, and zero browser console errors.
- Original structural selectors and 80 px source project typography remain in the generated document.
- Automated structural tests: 3 passed.

## Final result

passed
