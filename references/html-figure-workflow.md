# HTML Figure Workflow

Use this reference when creating editable HTML/CSS/SVG figure projects and when using Lavish for review.

## Recommended Project Structure

```text
figure-project/
  index.html
  styles.css
  assets/
    source-panel-a.png
    source-panel-b.png
  exports/
    figure.pdf
    figure.png
  data.csv or data.json
```

Keep files portable. Use relative paths from `index.html` to assets and styles.

## HTML/CSS/SVG Conventions

- Use semantic panel containers such as `<section class="panel panel-a">`.
- Use CSS grid for multi-panel layouts.
- Define design tokens in `:root`: figure width, font family, text sizes, line width, panel gap, and palette colors.
- Use SVG for diagrams, overlays, arrows, scale bars, labels, and chart-like vector content.
- Put empirical image panels in `<img>` elements and add annotations using positioned SVG overlays.
- Avoid external CDNs unless the user explicitly wants them. The figure should render offline.
- Add print CSS for stable page/export behavior.

## Lavish Refinement Loop

Lavish is the recommended fine-tuning step after the first complete HTML figure draft exists. Use it when the figure is structurally correct but needs human-guided polish: tighter spacing, better alignment, label wording, panel balance, arrow placement, color consistency, or small visual corrections that are hard to describe without pointing at the artifact.

1. Finish a coherent first HTML draft before starting Lavish. Do not use Lavish to replace scientific validation or data checking.
2. From the directory containing the figure project, run:

```bash
npx -y lavish-axi index.html
```

3. Ask the user to annotate elements, selected text, or layout regions directly in the browser.
4. Poll for feedback when running an interactive agent loop:

```bash
npx -y lavish-axi poll index.html
```

5. Revise `index.html`, `styles.css`, SVG layers, and local assets based on the precise feedback.
6. Repeat until layout warnings and user review feedback are resolved.

Use relative asset paths. Avoid root-prefixed paths such as `/assets/image.png`, which may fail in local artifact routes.

## Export Guidance

Prefer browser-based export from the rendered HTML:

- PDF for vector-preserving review and manuscript assembly
- PNG for preview and common submission workflows
- TIFF/EPS only when required by the target journal

When exporting PNG, set a large enough viewport or device scale factor to meet the intended effective resolution. Verify the export against the HTML source for clipped text, missing fonts, broken assets, and alignment shifts.

## Delivery Notes

When sending the result back to the user, include:

- source file paths
- export file paths if generated
- any source data or image limitations
- any author checks required before submission
