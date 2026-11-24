# Academic Figure Standards

Use this reference when selecting figure width, typography, stroke weight, spacing, color palettes, and export parameters for publication-style figures.

## Target Width By Venue

Establish the exact target paper width before creating CSS variables or SVG viewBoxes (`1 mm = 3.7795 CSS px` at `96 dpi`, `1 in = 25.4 mm = 96 px`).

| Venue / Format | Single-Column | Intermediate / 1.5-Col | Double-Column / Full Width |
| --- | --- | --- | --- |
| **Nature** | `89 mm` (`336 px`) | `120–136 mm` (`454–514 px`) | `183 mm` (`692 px`) |
| **Science** | `55 mm` (`208 px`) | `120 mm` (`454 px`) | `183 mm` (`692 px`) |
| **Cell** | `85 mm` (`321 px`) | `114 mm` (`431 px`) | `174 mm` (`658 px`) |
| **NeurIPS** | — | — | `139.7 mm` (`5.5 in`, `528 px`) |
| **ICML / ICLR / CVPR / IEEE** | `82–85 mm` (`3.25 in`, `310–321 px`) | — | `171–178 mm` (`6.75–7.0 in`, `646–673 px`) |

> Default template width is `178 mm` (`~673 px`, 2 columns with `7 mm` gap → `~323 px` per column). Override `--figure-width` in `:root` to match the target venue.

## Typography And Stroke Specifications

Use physical `pt` units in CSS (`1 pt = 1.3333 px` at `96 dpi`) and keep SVG `viewBox` dimensions matched `1:1` with rendered CSS pixel size so fonts do not shrink unintentionally.

| Role | Recommended Size / Weight | Minimum Floor | Notes |
| --- | --- | --- | --- |
| **Panel labels (`A`, `B`, `C`)** | `9–10 pt`, Bold (`700`) | `8 pt` | Uppercase (Nature/Cell/ML) or lowercase per journal style |
| **Panel titles / headings** | `8–9 pt`, Bold (`600–700`) | `7.5 pt` | Keep short (2–5 words) |
| **Axis titles, labels, legends** | `7–8 pt`, Regular–Medium | `6.5 pt` | Single font family across all panels |
| **Tick labels, notes, callouts** | `6–7 pt`, Regular (`400`) | `5.5–6 pt` | Never allow rendered SVG text below `5.5 pt` |
| **Axis spines & diagram borders** | `0.5–0.75 pt` | `0.5 pt` | Avoid hairline `< 0.35 pt` strokes in print |
| **Data curves & primary arrows** | `1.0–1.5 pt` | `0.75 pt` | Scale arrowheads proportionally |
| **Subtle gridlines / guides** | `0.35–0.5 pt` | `0.3 pt` | Light neutral gray (`#E0E3E7`) |

- Use conservative sans-serif fonts: `Arial`, `Helvetica`, `Liberation Sans`, `Source Sans 3`, or `Inter`.
- Use a single type family across HTML headings, SVG diagrams, and embedded Matplotlib/data plots unless the venue requires otherwise.
- Avoid decorative fonts, negative letter spacing, and viewport-scaled (`vw`/`vh`) font sizes.

## Layout And Panels

- Lock `.paper-figure` to the exact target `--figure-width` rather than reflowing columns on narrow viewports.
- Use strict alignment for panel edges, labels, axes, legends, and annotation baselines.
- Use consistent panel gaps (`5–8 mm`) and outer margins.
- Keep panel labels (`A`, `B`, `C`, `D`) in the same relative corner, usually upper-left.
- Avoid nested card-like UI decoration, heavy drop shadows, or rounded app-style chrome.
- Prefer whitespace over boxes; use borders only when they clarify image bounds or module grouping.
- Do not let legends or annotations cover data points unless there is no better placement.

## Color-Blind-Safe Palettes

Use a unified palette of 4–8 colors, preserve color semantics for repeated concepts across panels, and ensure contrast works on white paper and in grayscale. Never rely on red/green contrast alone.

### Okabe-Ito Categorical Palette (Default)

| Semantic Role | HEX | Preview Intent |
| --- | --- | --- |
| Blue (Primary / Method A) | `#0072B2` | High-contrast primary series |
| Teal (Secondary / Method B) | `#009E73` | Safe contrast against blue & orange |
| Vermilion / Orange (Highlight / Method C) | `#D55E00` | Warm accent, distinct from green/teal |
| Orange-Gold (Baseline / Method D) | `#E69F00` | Warm amber |
| Reddish-Purple (Method E) | `#CC79A7` | Distinct magenta-purple |
| Sky Blue (Aux / Background series) | `#56B4E9` | Lighter cool series |
| Primary Ink / Axis / Muted | `#202124` / `#3C4043` / `#5F6368` | Structure, baselines, muted comparisons |

### Paul Tol Muted Palette (Dense Multi-Series)

Use when 6–8 distinct curves or categories are needed without harsh saturation:
- Indigo `#332288`, Cyan `#88CCEE`, Teal `#44AA99`, Green `#117733`, Sand `#DDCC77`, Rose `#CC6677`, Wine `#882255`, Purple `#AA4499`.

### Muted Structural Tints (Diagram Modules & Bands)

Pair solid accents with light fills for diagram blocks and confidence regions:
- Blue tint `#E8F2F8`, Teal tint `#E6F5F0`, Orange tint `#FAEDE4`, Gold tint `#FCF4E1`, Neutral surface `#F3F5F6`.

## Raster, Vector, And Resolution

- Keep diagrams, axes, labels, arrows, and statistical plots in vector SVG/PDF (`svg.fonttype = 'none'` when exporting from Matplotlib so text remains editable and selectable).
- Keep original raster evidence (microscopy, MRI/fMRI, gels, photos) in `assets/` and overlay labels/scale bars in separate vector SVG/HTML layers.
- Export PNG at **at least 300 dpi** (`600 dpi` when mixing dense line art and raster details).
- Avoid scaling low-resolution screenshots beyond their native useful size; state source resolution limitations if only a screenshot exists.

## Export Expectations

- Treat HTML/CSS/SVG (plus source `data.csv`/`data.json` or plotting scripts) as the editable source.
- Always ensure CSS preserves fill and background colors during print/PDF export (`print-color-adjust: exact`).
- Export tightly cropped vector PDF (no full-page A4 whitespace) for manuscript assembly and archival review.
- Export high-resolution PNG for visual inspection and submission portals; TIFF/EPS only when explicitly required by a journal.
- Inspect the rendered PNG and audit results before delivery.
