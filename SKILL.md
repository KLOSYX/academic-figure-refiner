---
name: academic-figure-refiner
description: Refine, rebuild, and prepare publication-ready academic figures from reference images, draft diagrams, screenshots, plots, or multi-panel layouts. Use when Codex needs to improve paper figures, scientific illustrations, HTML/SVG figure artifacts, neuroscience or behavioral task diagrams, correlation matrices, brain/imaging panels, data charts, or journal-style exports while preserving scientific meaning and producing editable HTML/CSS/SVG sources with PDF/PNG export guidance.
---

# Academic Figure Refiner

Create publication-ready academic figures from reference images or rough drafts using an HTML-first workflow. Treat HTML/CSS/SVG as the editable source, preserve scientific meaning before improving appearance, and export paper-friendly PDF/PNG deliverables when requested.

## Core Workflow

1. **Classify the figure.** Identify whether the source is a data chart, multi-panel figure, mechanism diagram, behavioral task flow, correlation matrix, imaging panel, image panel, or mixed figure. For detailed recipes, read `references/figure-recipes.md`.
2. **Protect scientific content.** Before aesthetic edits, list the elements that must not change: data values, trends, axes, labels, units, group names, statistical annotations, experimental conditions, scale bars, image evidence, and panel relationships. For integrity rules, read `references/scientific-integrity.md`.
3. **Choose the rebuild strategy.**
   - Prefer code redraw for diagrams, layouts, charts with source data, task flows, labels, legends, arrows, overlays, and multi-panel assembly.
   - Preserve original raster evidence for microscopy, MRI/fMRI, gels, histology, photos, or other empirical images. Add labels/scale bars/annotations as separate SVG or HTML overlay layers.
   - Use generative image editing only for explicitly requested non-evidence visuals or schematic/illustrative elements. Do not use it to invent, alter, remove, or "clean up" scientific evidence.
4. **Build an editable figure project.** Default structure:
   - `index.html` as the source figure
   - `styles.css` for typography, spacing, colors, and panel rules
   - `assets/` for original images and local resources
   - `exports/figure.pdf` and `exports/figure.png` after export
   - optional `data.csv` or `data.json` for data-backed charts
5. **Apply academic styling.** Use restrained typography, consistent spacing, color-blind-aware palettes, stable panel labels, and print-safe line weights. For standards, read `references/academic-standards.md`.
6. **Review visually.** Inspect the rendered figure at the target paper width and at a smaller preview size. Fix text overflow, clipped labels, inconsistent alignment, low-resolution assets, and overcrowding.
7. **Optionally use Lavish for feedback.** If available, open the HTML artifact with `npx -y lavish-axi index.html`, collect element-level annotations or layout warnings, revise the source, and repeat. Lavish is recommended for human review but is not required. For details, read `references/html-figure-workflow.md`.
8. **Export and report.** Export PDF for vector-preserving review and PNG for quick submission or preview. Mention any scientific assumptions, data approximations, source image limitations, or edits that require author verification.

## HTML-First Rules

- Use the bundled `assets/html-figure-template/` as a starting point when creating a new figure project.
- Keep layout and styling in CSS; keep SVG markup readable and grouped by semantic layer.
- Use relative asset paths such as `assets/source-panel-b.png`; avoid root-prefixed paths because local artifact viewers and Lavish may not resolve them.
- Prefer SVG for labels, arrows, scale bars, schematic shapes, and vector diagrams.
- Keep empirical rasters separate from annotations. Do not bake labels into raw images unless the user explicitly asks for a flat export.
- Avoid heavy front-end frameworks for v1 figure artifacts unless the user already has a project requiring them.

## Quality Gate

Before delivery, verify:

- The figure's scientific claim, data trend, labels, units, statistics, and panel relationships are unchanged or explicitly author-approved.
- All text remains readable at target single-column or double-column width.
- Panel labels are consistent and aligned.
- Colors are unified, accessible, and not dependent on red/green contrast alone.
- Axes, legends, scale bars, and captions/labels are complete where applicable.
- Lines, arrows, and markers are not too thin for print.
- PDF/PNG exports match the HTML source and no text is clipped or overlapping.
- Any data reconstructed from a screenshot is clearly marked as approximate and requiring verification.

## Useful Prompts

- "Use $academic-figure-refiner to rebuild this rough behavioral task diagram as an editable HTML figure for a neuroscience paper."
- "Use $academic-figure-refiner to turn this multi-panel draft into a clean journal-style figure with consistent panel labels and colors."
- "使用 $academic-figure-refiner，把这张参考图改成论文风格的 HTML/SVG 图，保留科学含义并导出 PDF 和 PNG。"
