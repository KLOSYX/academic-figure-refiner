---
name: academic-figure-refiner
description: Build, refine, rebuild, and prepare publication-ready academic figures from scratch, manuscript context, study descriptions, data, reference images, draft diagrams, screenshots, plots, or multi-panel layouts. Use when Codex needs to create new paper figures, improve existing figures, produce scientific illustrations, HTML/SVG figure artifacts, neuroscience or behavioral task diagrams, correlation matrices, brain/imaging panels, data charts, or journal-style exports while preserving scientific meaning and producing editable HTML/CSS/SVG sources with PDF/PNG export guidance and Lavish-assisted human-in-the-loop refinement.
---

# Academic Figure Builder and Refiner

Create publication-ready academic figures from scientific intent, manuscript context, data, reference images, or rough drafts using an HTML-first workflow. Treat HTML/CSS/SVG as the editable source, preserve scientific meaning before improving appearance, and use Lavish as the preferred human-in-the-loop layer for precise refinement after the first complete figure draft.

## Core Workflow

1. **Choose the entry path.** Decide whether the task is a from-scratch build or reference-based refinement.
   - For from-scratch builds, clarify the figure purpose, audience, paper context, target width, intended panels, available data, empirical evidence, labels, and required scientific claims.
   - For reference-based refinement, identify which visual structure, data, labels, and scientific meaning must be preserved.
2. **Classify the figure.** Identify whether the target is a data chart, multi-panel figure, mechanism diagram, behavioral task flow, correlation matrix, imaging panel, image panel, or mixed figure. For detailed recipes, read `references/figure-recipes.md`.
3. **Protect scientific content.** Before aesthetic edits, list the elements that must not change: data values, trends, axes, labels, units, group names, statistical annotations, experimental conditions, scale bars, image evidence, and panel relationships. For integrity rules, read `references/scientific-integrity.md`.
4. **Choose the build or rebuild strategy.**
   - Prefer code redraw for diagrams, layouts, charts with source data, task flows, labels, legends, arrows, overlays, and multi-panel assembly.
   - Preserve original raster evidence for microscopy, MRI/fMRI, gels, histology, photos, or other empirical images. Add labels/scale bars/annotations as separate SVG or HTML overlay layers.
   - Use generative image editing only for explicitly requested non-evidence visuals or schematic/illustrative elements. Do not use it to invent, alter, remove, or "clean up" scientific evidence.
5. **Build an editable first draft.** Default structure:
   - `index.html` as the source figure
   - `styles.css` for typography, spacing, colors, and panel rules
   - `assets/` for original images and local resources
   - `exports/figure.pdf` and `exports/figure.png` after export
   - optional `data.csv` or `data.json` for data-backed charts
6. **Apply academic styling.** Use restrained typography, consistent spacing, color-blind-aware palettes, stable panel labels, and print-safe line weights. For standards, read `references/academic-standards.md`.
7. **Review visually.** Inspect the rendered figure at the target paper width and at a smaller preview size. Fix text overflow, clipped labels, inconsistent alignment, low-resolution assets, and overcrowding.
8. **Use Lavish for human-in-the-loop refinement when possible.** After the first complete HTML figure draft is rendered, open it with `npx -y lavish-axi index.html` so the user can click elements, select text, and mark precise layout or style changes. Poll the feedback, revise the HTML/CSS/SVG source, and repeat until the figure is usable, readable, and polished. Lavish is the preferred loop for details that are hard to express in text, but it does not replace scientific validation. Always read `references/html-figure-workflow.md` before running Lavish because the CLI has long-polling and local-server pitfalls.
9. **Export and report.** Export PDF for vector-preserving review and PNG for quick submission or preview. Mention any scientific assumptions, data approximations, source image limitations, or edits that require author verification.

## HTML-First Rules

- Use the bundled `assets/html-figure-template/` as a starting point when creating a new figure project.
- Keep layout and styling in CSS; keep SVG markup readable and grouped by semantic layer.
- Use relative asset paths such as `assets/source-panel-b.png`; avoid root-prefixed paths because local artifact viewers and Lavish may not resolve them.
- Prefer SVG for labels, arrows, scale bars, schematic shapes, and vector diagrams.
- Keep empirical rasters separate from annotations. Do not bake labels into raw images unless the user explicitly asks for a flat export.
- Avoid heavy front-end frameworks for v1 figure artifacts unless the user already has a project requiring them.

## From-Scratch Figure Planning

When no reference figure exists, build a compact figure plan before writing HTML:

- intended paper claim or communication goal
- figure type and panel list
- required data, images, labels, units, and statistics
- target audience and journal/presentation context
- target width and expected export format
- what the user must verify before the figure can be treated as submission-ready

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
- "Use $academic-figure-refiner to build a new multi-panel academic figure from this study description and dataset, then refine it with Lavish."
- "Use $academic-figure-refiner to turn this multi-panel draft into a clean journal-style figure with consistent panel labels and colors."
- "使用 $academic-figure-refiner，从实验流程和数据开始构建论文图，生成 HTML 初稿后用 Lavish 做人在循环精修。"
