# Academic Figure Builder and Refiner

Academic Figure Builder and Refiner is an agent skill for creating polished, publication-ready academic figures from scratch or improving existing reference images, rough drafts, screenshots, data tables, and multi-panel layouts.

The workflow is HTML-first with hybrid data plotting: use HTML/CSS/SVG (plus Python/JS plotting scripts for real data) as the editable source, preserve scientific meaning, run automated layout auditing and tightly cropped PDF/PNG export via `scripts/export_figure.py`, visually inspect the rendered PNG, and optionally use [Lavish](https://github.com/kunchenguid/lavish-axi) for interactive human-in-the-loop polish.

## Installation

Install with the open agent skills CLI:

```bash
npx skills add KLOSYX/academic-figure-refiner
```

This repository is structured as a single root skill: `SKILL.md` sits at the repository root, with `scripts/`, `references/`, `assets/`, and `agents/` beside it.

For a manual install, clone the repo into your personal skills directory:

```bash
git clone https://github.com/KLOSYX/academic-figure-refiner.git ~/.agents/skills/academic-figure-refiner
# or for Codex:
git clone https://github.com/KLOSYX/academic-figure-refiner.git ~/.codex/skills/academic-figure-refiner
```

### Dependencies for Automated Export

`scripts/export_figure.py` uses Python 3 + `playwright` and either Playwright's Chromium or a local Google Chrome / Chromium installation:

```bash
pip install playwright
# Optional if Google Chrome / Chromium is not already installed locally:
playwright install chromium
```

## What It Does

- Builds publication-width figures for Nature, Science, Cell, NeurIPS, ICML/ICLR, CVPR, and IEEE layouts.
- Enforces `1:1` SVG physical coordinates and `pt`-unit typography so labels never shrink silently at print width.
- Combines hand-authored vector diagrams/pipelines with script-generated data plots (`matplotlib`/`seaborn` `svg.fonttype = 'none'`) and separate SVG overlays for empirical rasters.
- Covers general science, neuroscience/behavioral diagrams, microscopy/imaging panels, and AI/ML figures (model architectures, agent pipelines, scaling/ablation curves, Pareto frontiers, SVG math notation).
- Automates tightly cropped vector PDF + high-DPI (`>= 300 dpi`) PNG export and runs DOM/SVG audits (broken images, minimum rendered font `pt`, boundary clipping, label overlap).
- Supports optional [Lavish](https://github.com/kunchenguid/lavish-axi) human-in-the-loop visual polish when Node/`npx` is available.

## Quick Export & Audit

Use the bundled export script with Playwright (or system Chrome fallback):

```bash
python3 scripts/export_figure.py path/to/figure/index.html --dpi 300
```

Common options:
- `--audit-only`: check broken `<img>` tags, effective SVG font size (`>= 5.5 pt`), clipping, and text overlap without writing files.
- `--format pdf|png|both`: select output formats (default `both`).
- `--pad-mm 2.0`: adjust PDF crop padding around `.paper-figure`.
- `--dpi 600`: raise PNG resolution for dense line art or microscopy overlays.

## Typical Project Output

```text
figure-project/
  index.html
  styles.css
  plot_panels.py        # Optional data-plotting script
  data.csv / data.json  # Verified source data
  assets/
  exports/
    figure.pdf
    figure.png
```

## Three-Tier Review & Optional Lavish Loop

1. **Tier 1 (Default Mandatory)**: Run `scripts/export_figure.py`, verify the automated SVG/DOM audit passes, and inspect `exports/figure.png` directly.
2. **Tier 2 (Static Browser Preview)**: Open `index.html` in a local browser to review screen and print rendering.
3. **Tier 3 (Optional Lavish Interactive Polish)**: When Node/`npx` is available and fine visual tweaks are easier to point at directly:

```bash
npx -y lavish-axi index.html
npx -y lavish-axi poll index.html
```

After updating HTML/CSS/SVG from Lavish feedback, re-run `scripts/export_figure.py` to regenerate final PDF/PNG deliverables. See `references/html-figure-workflow.md` for port/polling notes.

## Skill Contents

- `SKILL.md`: main workflow, hybrid build rules, and quantitative quality gate.
- `scripts/export_figure.py`: tightly cropped vector PDF & high-DPI PNG exporter with automated layout audit.
- `references/academic-standards.md`: venue widths, typography/stroke tables, and Okabe-Ito / Paul Tol color palettes.
- `references/scientific-integrity.md`: data plotting integrity and evidence preservation rules.
- `references/figure-recipes.md`: figure-type recipes (including AI/ML architectures, scaling curves, and SVG math notation).
- `references/html-figure-workflow.md`: 1:1 SVG coordinate rule, Matplotlib-to-HTML assembly, export usage, and Lavish loop.
- `assets/html-figure-template/`: 1:1-scaled, print-safe two-panel HTML/CSS starter.

## Example Prompts

```text
Use /academic-figure-refiner to build a multi-panel NeurIPS figure combining an agent pipeline diagram in Panel A and scaling curves from results.csv in Panel B, then audit and export PDF/PNG.
```

```text
使用 /academic-figure-refiner，将这张草图重构为符合 Nature 双栏宽度（183 mm）的可编辑 HTML/SVG 图，并导出紧贴裁边的矢量 PDF 和 300 DPI PNG。
```
