---
name: academic-figure-refiner
description: Build, refine, rebuild, and prepare publication-ready academic figures from scratch, manuscript context, study descriptions, data, reference images, draft diagrams, screenshots, plots, or multi-panel layouts. Use when creating new paper figures, improving existing figures, producing scientific or AI/ML architecture illustrations, HTML/SVG figure artifacts, scaling/ablation plots, behavioral task diagrams, correlation matrices, brain/imaging panels, or journal-style exports while preserving scientific meaning and producing editable HTML/CSS/SVG sources with automated PDF/PNG export, layout auditing, and optional Lavish refinement.
---

# Academic Figure Builder and Refiner

Create publication-ready academic figures from scientific intent, manuscript context, data, reference images, or rough drafts using an HTML-first workflow. Treat HTML/CSS/SVG (and backing data/plotting scripts) as the editable source, preserve scientific meaning before improving appearance, export tightly cropped PDF/PNG via `scripts/export_figure.py`, visually inspect every render, and optionally use Lavish for human-in-the-loop polish.

## Core Workflow

1. **Choose the entry path.** Decide whether the task is a from-scratch build or reference-based refinement.
   - For from-scratch builds, clarify the figure purpose, audience, paper/venue context, target physical width (e.g., single-column `85–89 mm`, NeurIPS `139.7 mm`, double-column `178–183 mm`), intended panels, available data, empirical evidence, labels, and required scientific claims.
   - For reference-based refinement, identify which visual structure, data, labels, and scientific meaning must be preserved.
2. **Classify the figure.** Identify whether the target is a multi-panel figure, mechanism diagram, AI/ML architecture or agent pipeline, behavioral task flow, statistical/scaling/ablation chart, correlation matrix, imaging/microscopy panel, or mixed figure. Read `references/figure-recipes.md` for figure-type recipes.
3. **Protect scientific content.** Before aesthetic edits, list the elements that must not change: data values, trends, axes, labels, units, group names, statistical annotations, experimental conditions, scale bars, image evidence, and panel relationships. Read `references/scientific-integrity.md` for integrity rules.
4. **Choose the hybrid build strategy.**
   - **Diagrams, pipelines, labels, arrows & overlays**: hand-author clean vector SVG inside the HTML grid.
   - **Statistical charts, scaling/ablation curves, heatmaps & dense matrices**: generate vector SVG panels programmatically from `data.csv`/`data.json` (e.g., Python `matplotlib`/`seaborn` with `rcParams['svg.fonttype'] = 'none'`, sized to target column inches, or deterministic inline JS) rather than hand-calculating SVG coordinates.
   - **Empirical raster evidence** (microscopy, MRI/fMRI, gels, photos): preserve original raster files untouched in `assets/` and add labels, arrows, ROIs, and scale bars as separate SVG overlay layers.
   - **Generative image editing**: only for explicitly requested non-evidence visuals or schematic illustrations—never to invent, alter, remove, or "clean up" scientific evidence.
5. **Build an editable first draft at 1:1 physical scale.**
   - Start from `assets/html-figure-template/` (`index.html`, `styles.css`).
   - Lock `--figure-width` in `:root` to the venue width (`mm`), use physical `pt` units for typography and strokes, and match each SVG `viewBox` width `1:1` to its rendered CSS pixel column width at `96 dpi` (`1 mm = 3.7795 px`) so labels do not shrink unexpectedly.
   - Default project structure:
     - `index.html` and `styles.css` as the layout and vector assembly source
     - `assets/` for original raster images, generated plot SVGs, and local resources
     - `data.csv` / `data.json` and optional `plot_panels.py` for data-backed charts
     - `exports/figure.pdf` and `exports/figure.png`
6. **Apply quantitative academic standards.** Use restrained sans-serif typography (`5.5–6 pt` minimum rendered floor; `7–8 pt` axis/body; `9–10 pt bold` panel labels), color-blind-safe palettes (Okabe-Ito / Paul Tol), print-safe strokes (`0.5–1.5 pt`), and strict alignment. Read `references/academic-standards.md` for venue width tables, font/stroke limits, and HEX palettes.
7. **Export, audit, and visually inspect (mandatory).**
   - Run `scripts/export_figure.py index.html --dpi 300` (see `references/html-figure-workflow.md`) to generate tightly cropped vector PDF + high-DPI PNG and automatically check for broken images, effective SVG font sizes `< 5.5 pt`, boundary overflow, and overlapping `<text>` elements.
   - Open and inspect `exports/figure.png` directly to verify spacing, alignment, legend balance, contrast, and print legibility. Fix any layout issues and re-export.
8. **Optional human-in-the-loop polish.**
   - Review `index.html` in a browser preview, or—when Node/`npx` is available—launch `npx -y lavish-axi index.html` and poll feedback (`npx -y lavish-axi poll index.html`) for precise click-and-annotate layout tweaks. Always read `references/html-figure-workflow.md` before running Lavish, and re-run `scripts/export_figure.py` after any Lavish edits.
9. **Deliver and report.** Provide source and export paths, exact dimensions/DPI, audit status, and clearly note any scientific assumptions, approximated data from screenshots, source image limits, or author checks required before submission.

## HTML-First Rules

- Use `assets/html-figure-template/` as the starting point for new figure projects.
- Lock `.paper-figure` to `var(--figure-width)`—never collapse multi-panel grids into a single column on narrow viewports (`@media (max-width: ...)`), as academic figures have fixed physical geometry.
- Keep `print-color-adjust: exact; -webkit-print-color-adjust: exact;` and `@page { margin: 0; }` so vector PDF exports preserve fills and crop cleanly.
- Use relative asset paths such as `assets/source-panel-b.png`; avoid root-prefixed paths (`/assets/...`).
- Keep empirical rasters separate from SVG annotation overlays; do not bake labels into raw images unless explicitly requested.
- Avoid external CDNs and heavy front-end frameworks unless the user's project requires them.

## From-Scratch Figure Planning

When no reference figure exists, build a compact figure plan before writing HTML:

- intended paper claim or communication goal
- venue/context, target width (`mm`), and expected export formats
- panel list and figure type per panel (diagram vs. data script vs. raster + overlay)
- required source data files, images, labels, units, and statistics
- what the author must verify before treating the figure as submission-ready

## Quality Gate

Before delivery, verify every item:

- Scientific claim, data values/trends, labels, units, statistics, and panel relationships are faithful to source data or explicitly author-approved; any values reconstructed from a screenshot are clearly flagged as approximate.
- Automated audit (`scripts/export_figure.py`) passes with zero broken `<img>` elements, zero text clipping/overflow, zero overlapping `<text>` labels, and minimum rendered SVG font size `>= 5.5–6 pt` at target width.
- Panel labels (`A`, `B`, `C`, ...) are consistent in size, weight, and upper-left placement; colors use a unified color-blind-safe palette (not red/green alone).
- Lines, arrows, and markers meet print minimums (`>= 0.5 pt` spines/borders, `>= 0.75–1.5 pt` curves/arrows).
- `exports/figure.pdf` is tightly cropped with preserved background/fill colors (no A4 margin whitespace), and `exports/figure.png` (`>= 300 dpi`) has been visually inspected and matches the HTML source.

## Useful Prompts

- "Use `/academic-figure-refiner` to rebuild this rough model architecture diagram as an editable HTML/SVG figure at NeurIPS width (139.7 mm) and export PDF/PNG."
- "Use `/academic-figure-refiner` to assemble a two-panel Nature-style figure (183 mm) combining an SVG agent pipeline in Panel A with a scaling curve plotted from `results.csv` in Panel B."
- "Use `/academic-figure-refiner` to turn this multi-panel draft into a clean journal-style figure with consistent panel labels, Okabe-Ito colors, and >=300 dpi exports."
- "使用 `/academic-figure-refiner`，基于实验流程描述和 `data.csv` 构建双栏论文主图，自动审计排版后导出紧贴裁边的矢量 PDF 与 300 DPI PNG。"
