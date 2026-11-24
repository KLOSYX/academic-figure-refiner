# HTML Figure Workflow

Use this reference when building editable HTML/CSS/SVG figure projects, integrating data-driven plots, running automated export & layout audits, and optionally polishing with Lavish.

## Recommended Project Structure

```text
figure-project/
  index.html
  styles.css
  plot_panels.py        # Optional: generates data-driven SVG panels from data.csv/json
  data.csv / data.json  # Source data for charts and matrices
  assets/
    panel-b-plot.svg    # Generated data plot or preserved raster evidence
    source-panel-c.png
  exports/
    figure.pdf          # Tightly cropped vector PDF
    figure.png          # High-DPI PNG (>= 300 dpi)
```

Keep files portable. Use relative paths from `index.html` to `styles.css`, `assets/`, and scripts. Never use root-prefixed paths such as `/assets/image.png`.

## The 1:1 SVG Physical Coordinate Rule

A common failure mode in HTML figures is mismatched SVG `viewBox` scale: if a column renders at `323 CSS px` (`~85.5 mm` at `96 dpi`) and its `<svg>` uses `viewBox="0 0 640 260"`, the browser scales the SVG down by `~0.5×`, shrinking `11 px` text to `5.5 px` (`~4.1 pt`)—unreadable in print.

Always match each SVG `viewBox` width to its actual rendered CSS column width at `96 dpi` (`1 mm = 3.7795 px`):

- Full double-column (`178 mm`): `~673 px` (`viewBox="0 0 673 H"`)
- Half of a 2-column `178 mm` figure with `7 mm` gap: `(178 - 7) / 2 = 85.5 mm` → `~323 px` (`viewBox="0 0 323 H"`)
- Single-column Nature (`89 mm`): `~336 px` (`viewBox="0 0 336 H"`)
- NeurIPS full width (`139.7 mm`): `~528 px` (`viewBox="0 0 528 H"`)

When `viewBox` width matches rendered CSS pixels `1:1`, physical `pt` tokens (`--body-size: 7.5pt`, `--tick-size: 6.5pt`) render at exact publication size.

## HTML/CSS/SVG Conventions

- Use semantic panel containers such as `<section class="panel panel-a">`.
- Use CSS Grid (`.paper-figure`) locked to `var(--figure-width)`—never collapse columns on narrow screen viewports (`@media (max-width: ...)`), because figures have fixed physical aspect ratios; use `overflow-x: auto` on `.figure-page` instead.
- Define design tokens in `:root`: `--figure-width`, `--font-sans`, physical `pt` font sizes, print-safe stroke weights, and color-blind-safe palette hex codes.
- Include `print-color-adjust: exact; -webkit-print-color-adjust: exact;` globally and `@page { margin: 0; }` for print/PDF fidelity.
- Put empirical raster images in `<img>` elements and add annotations (arrows, ROIs, scale bars) in an overlaid `<svg>` positioned over the image container.
- Avoid external CDNs so figures render cleanly offline and inside sandboxed headless browsers.

## Hybrid Data Script + HTML Assembly Workflow

Do **not** hand-calculate SVG paths for complex statistical charts (error bands, KDEs, dense scatters, correlation heatmaps). Instead:

1. Generate data panels from `data.csv` / `data.json` with Python (`matplotlib` / `seaborn`), keeping fonts editable (`svg.fonttype = 'none'`) and matching the target panel width in inches:

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "svg.fonttype": "none",          # Keep text as <text> nodes, not outlined paths
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans"],
    "font.size": 7.5,
    "axes.titlesize": 8.5,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "axes.linewidth": 0.75,
})

# Example: half-panel width 85.5 mm = 3.366 in
fig, ax = plt.subplots(figsize=(3.366, 2.1))
# ... plot from verified data ...
fig.savefig("assets/panel-b-plot.svg", transparent=True, bbox_inches="tight")
```

2. Embed `assets/panel-b-plot.svg` in HTML (`<img src="assets/panel-b-plot.svg" ...>` or inline `<svg>`) alongside hand-crafted SVG architecture diagrams and shared panel labels (`A`, `B`, `C`).
3. Alternatively, for dynamic lightweight figures, read `data.json` via inline JavaScript to build SVG elements deterministically.

## Automated Export And Layout Audit

Use the bundled export script (`scripts/export_figure.py`) from the skill directory to export tightly cropped vector PDF + high-DPI PNG and catch layout bugs automatically (use your virtual environment's Python if `playwright` is installed in a venv):

```bash
# Standard export (PDF + 300 dpi PNG + SVG audit)
python3 <skill_dir>/scripts/export_figure.py index.html

# Custom DPI, output directory, or PNG-only
python3 <skill_dir>/scripts/export_figure.py index.html --dpi 600 --out-dir exports --format both

# Audit layout without writing files
python3 <skill_dir>/scripts/export_figure.py index.html --audit-only
```

What the script checks automatically:
- **Broken images**: verifies every `<img>` finishes loading with `naturalWidth > 0`.
- **Effective SVG font size**: inspects `getComputedStyle(text).fontSize` scaled by `getScreenCTM()` to catch hidden `viewBox` shrinkages below `--min-font-pt` (default `5.5 pt`).
- **Clipping / boundary overflow**: flags any `<text>` extending outside `.paper-figure`.
- **Label collisions**: checks pairwise bounding-box overlaps among `<text>` nodes in each SVG.
- **Tight PDF crop**: measures `.paper-figure` in print media mode and exports an exact-size PDF page (plus `--pad-mm`, default `2.0 mm`) with no A4 margins and preserved background fills.

After running `export_figure.py`, **always inspect `exports/figure.png` visually** (with `read_file` or an image viewer) to verify spacing, alignment, legend balance, and typography before delivering or moving to human review.

## Three-Tier Review & Refinement Loop

1. **Tier 1 — Automated Audit + Visual Self-Check (Mandatory)**:
   Run `scripts/export_figure.py`, fix any reported small text, clipping, broken images, or overlapping labels, and inspect the exported PNG visually.
2. **Tier 2 — Local Static Preview (Always Available)**:
   Open `index.html` in a local browser (or browser preview pane) to inspect print/screen layout and copy-paste readability.
3. **Tier 3 — Lavish Human-in-the-Loop Polish (Optional, when Node/`npx` is available)**:
   After a complete, scientifically faithful HTML draft passes Tier 1, use [Lavish](https://github.com/kunchenguid/lavish-axi) for interactive click-and-annotate refinement (tightening spacing, alignment, label wording, arrow placement, visual hierarchy):

```bash
npx -y lavish-axi index.html
npx -y lavish-axi poll index.html
```

After patching `index.html` or `styles.css` from Lavish feedback:

```bash
npx -y lavish-axi poll index.html --agent-reply "Updated spacing and label alignment; please review."
```

When finished, re-run `scripts/export_figure.py` to regenerate final PDF/PNG deliverables.

### Lavish CLI Notes And Pitfalls

- `npx -y lavish-axi --help` prints playbook guidance and confirms the intended workflow.
- Lavish serves the HTML through a local Express server (typically port `4387`). Treat the returned URL as the review surface, not the final artifact URL.
- Keep all CSS, images, fonts, and scripts reachable via relative paths next to `index.html`.
- `poll` is intentionally blocking; do not add `--timeout-ms` in normal interactive loops.
- If a harness times out a foreground `poll`, rerun `lavish-axi poll <html-file>` — queued feedback is preserved.
- If `poll` returns `SERVER_ERROR`, rerun `lavish-axi <html-file>` and then poll again.
- If port `4387` reports `EADDRINUSE`, inspect stale processes with `lsof -nP -iTCP:4387 -sTCP:LISTEN` (`lavish-axi stop` may report `not-running` even when a node process still listens).
- `lavish-axi end <html-file>` can fail when no server is reachable; prefer ending from the active session.
- Keep `<meta name="lavish-live-reload" content="root" />` in `<head>` for live reload, while keeping the HTML completely portable without Lavish.

## Delivery Checklist

When reporting back to the user, include:
- Source file paths (`index.html`, `styles.css`, data/plotting scripts, `assets/`)
- Export file paths (`exports/figure.pdf`, `exports/figure.png`) and exact physical dimensions / DPI
- Audit status and visual inspection summary
- Any data approximations, source image resolution limits, or checks the author must verify before submission
