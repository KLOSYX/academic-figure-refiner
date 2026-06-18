# Academic Figure Refiner

Academic Figure Refiner is a Codex skill for turning reference images, rough drafts, screenshots, and multi-panel layouts into polished, publication-ready academic figures.

The workflow is HTML-first: use HTML/CSS/SVG as the editable source, preserve scientific meaning, then export PDF and high-resolution PNG deliverables when needed.

## Installation

Install with the open agent skills CLI:

```bash
npx skills add KLOSYX/academic-figure-refiner
```

This repository is structured as a single root skill: `SKILL.md` sits at the repository root, with `references/`, `assets/`, and `agents/` beside it.

For a manual Codex install, clone the repo into your personal skills directory:

```bash
git clone https://github.com/KLOSYX/academic-figure-refiner.git ~/.codex/skills/academic-figure-refiner
```

Then invoke it in Codex with:

```text
Use $academic-figure-refiner to refine this paper figure.
```

## What It Does

- Rebuilds paper figures as editable HTML/CSS/SVG projects.
- Improves typography, spacing, panel labels, color consistency, and layout.
- Supports general academic figures with extra guidance for behavioral and neuroscience figures.
- Keeps empirical images separate from annotation overlays.
- Treats scientific integrity as the first constraint: no invented data, altered trends, removed evidence, or unsupported visual claims.
- Uses [Lavish](https://github.com/kunchenguid/lavish-axi) as a human-in-the-loop refinement pass after the first complete HTML draft.

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

After an initial HTML figure is complete, [Lavish](https://github.com/kunchenguid/lavish-axi) can be used for precise polish. The user can click elements, select text, and mark visual feedback directly in the browser, then Codex can revise the HTML/CSS/SVG source.

Lavish is not a replacement for the skill's first-pass figure construction. Use the skill to create a scientifically faithful first draft, then use Lavish as the fine-tuning loop for precise human feedback.

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
