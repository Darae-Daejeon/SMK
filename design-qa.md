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
