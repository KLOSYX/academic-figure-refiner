# Academic Figure Refiner

Academic Figure Refiner is a Codex skill for turning reference images, rough drafts, screenshots, and multi-panel layouts into polished, publication-ready academic figures.

The workflow is HTML-first: use HTML/CSS/SVG as the editable source, preserve scientific meaning, then export PDF and high-resolution PNG deliverables when needed.

## What It Does

- Rebuilds paper figures as editable HTML/CSS/SVG projects.
- Improves typography, spacing, panel labels, color consistency, and layout.
- Supports general academic figures with extra guidance for behavioral and neuroscience figures.
- Keeps empirical images separate from annotation overlays.
- Treats scientific integrity as the first constraint: no invented data, altered trends, removed evidence, or unsupported visual claims.
- Uses Lavish as a human-in-the-loop refinement pass after the first complete HTML draft.

## Typical Outputs

```text
figure-project/
  index.html
  styles.css
  assets/
  exports/
    figure.pdf
    figure.png
  data.csv or data.json
```

## Lavish Refinement

After an initial HTML figure is complete, Lavish can be used for precise polish. The user can click elements, select text, and mark visual feedback directly in the browser, then Codex can revise the HTML/CSS/SVG source.

```bash
npx -y lavish-axi index.html
npx -y lavish-axi poll index.html
```

Use Lavish for fine adjustments such as spacing, alignment, label wording, arrow placement, panel balance, and color consistency. Do not use it as a replacement for scientific validation or source-data checking.

## Skill Contents

- `SKILL.md`: main Codex workflow and quality gate.
- `references/academic-standards.md`: typography, layout, color, resolution, and export guidance.
- `references/scientific-integrity.md`: data and evidence preservation rules.
- `references/figure-recipes.md`: figure-type-specific guidance.
- `references/html-figure-workflow.md`: HTML/SVG conventions, Lavish loop, and export notes.
- `assets/html-figure-template/`: minimal two-panel HTML figure starter.

## Example Prompt

```text
Use $academic-figure-refiner to rebuild this rough behavioral task diagram as an editable HTML figure for a neuroscience paper, then use Lavish for final spacing and label refinements.
```
