# Academic Figure Standards

Use this reference when selecting typography, spacing, color, panel layout, and export conventions for publication-style figures.

## Typography

- Use conservative sans-serif fonts for most figures: Arial, Helvetica, Source Sans 3, Inter, or system sans-serif.
- Use a single type family unless the target journal or existing project demands otherwise.
- Keep font sizes hierarchical:
  - panel labels: largest and boldest
  - titles or short panel headings: medium
  - axis labels, legend labels, callouts: regular
  - tick labels and secondary notes: smallest readable size
- Avoid decorative fonts, negative letter spacing, and viewport-scaled font sizes.
- Ensure text remains readable after shrinking to the target paper width.

## Layout And Panels

- Use strict alignment for panel edges, labels, axes, legends, and annotation baselines.
- Use consistent panel gaps and outer margins.
- Keep panel labels such as A, B, C, D in the same relative position, usually upper-left.
- Avoid nested card-like decoration. Academic figures should feel composed, not like app UI.
- Prefer whitespace over boxes; use borders only when they clarify image bounds or panel grouping.
- Do not let legends or annotations cover data unless the reference already does and there is no better placement.

## Lines, Symbols, And Labels

- Use consistent line weights for axes, arrows, connectors, brackets, and panel dividers.
- Avoid hairline strokes that disappear in print.
- Keep arrowheads proportional to the line width and visual scale.
- Keep markers, error bars, confidence bands, significance brackets, and p-value labels consistent.
- Always preserve units, scale bars, condition labels, group names, and axis meanings.

## Color

- Use a small unified palette, normally 4-8 colors for a complex figure.
- Prefer restrained scientific palettes over highly saturated random colors.
- Do not rely on red/green contrast as the only encoding.
- Use neutral grays for structure and reserve accent colors for experimental conditions, important paths, or data groups.
- Keep repeated concepts the same color across panels.
- Ensure color choices work on white backgrounds and in grayscale when possible.

## Raster, Vector, And Resolution

- Prefer SVG/PDF for schematic diagrams, axes, labels, arrows, and charts.
- Use PNG/TIFF for raster evidence and final bitmap exports.
- Keep original raster data in `assets/` and annotate with separate vector overlays.
- For submission-style PNG exports, use at least 300 dpi equivalent; use higher effective resolution for line art or dense labels.
- Avoid scaling low-resolution screenshots beyond their useful size. If only a screenshot is available, state the limitation.

## Export Expectations

- Treat HTML/CSS/SVG as the editable source.
- Export PDF for vector-preserving review and archival handoff.
- Export high-resolution PNG for preview and common submission portals.
- Export TIFF/EPS only when required by a journal or user request.
- Verify exported files against the browser-rendered source before delivery.
