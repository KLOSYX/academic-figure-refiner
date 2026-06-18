# Academic Figure Builder and Refiner

Academic Figure Builder and Refiner is a Codex skill for creating polished, publication-ready academic figures from scratch or improving existing reference images, rough drafts, screenshots, and multi-panel layouts.

The workflow is HTML-first: use HTML/CSS/SVG as the editable source, preserve scientific meaning, create a coherent first draft, then use [Lavish](https://github.com/kunchenguid/lavish-axi) for human-in-the-loop refinement before exporting PDF and high-resolution PNG deliverables.

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
Use $academic-figure-refiner to build or refine this paper figure.
```

## What It Does

- Builds new academic figures from study descriptions, manuscript context, figure plans, data, and source images.
- Rebuilds paper figures as editable HTML/CSS/SVG projects.
- Improves typography, spacing, panel labels, color consistency, and layout.
- Supports general academic figures with extra guidance for behavioral and neuroscience figures.
- Keeps empirical images separate from annotation overlays.
- Treats scientific integrity as the first constraint: no invented data, altered trends, removed evidence, or unsupported visual claims.
- Uses [Lavish](https://github.com/kunchenguid/lavish-axi) as the preferred human-in-the-loop refinement pass after the first complete HTML draft.

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

## Human-in-the-Loop Refinement with Lavish

After an initial HTML figure is complete, [Lavish](https://github.com/kunchenguid/lavish-axi) can be used for precise polish. The user can click elements, select text, and mark visual feedback directly in the browser, then Codex can revise the HTML/CSS/SVG source.

Lavish is not a replacement for the skill's first-pass figure construction. Use the skill to create a scientifically faithful first draft, then use Lavish as the fine-tuning loop for precise human feedback that improves usability, readability, and publication fit.

```bash
npx -y lavish-axi index.html
npx -y lavish-axi poll index.html
```

Use Lavish for fine adjustments such as spacing, alignment, label wording, arrow placement, panel balance, visual hierarchy, small overlaps, readability at publication width, and color consistency. Do not use it as a replacement for scientific validation or source-data checking.

Practical notes from running Lavish locally:

- `lavish-axi index.html` opens or resumes a local review session and returns a `127.0.0.1` session URL.
- `lavish-axi poll index.html` is a blocking long-poll; silence is normal while waiting for user feedback.
- Use relative asset paths only. Root-prefixed paths such as `/assets/...` may not resolve.
- If port `4387` is stuck, check with `lsof -nP -iTCP:4387 -sTCP:LISTEN`.

## Skill Contents

- `SKILL.md`: main Codex workflow and quality gate.
- `references/academic-standards.md`: typography, layout, color, resolution, and export guidance.
- `references/scientific-integrity.md`: data and evidence preservation rules.
- `references/figure-recipes.md`: figure-type-specific guidance.
- `references/html-figure-workflow.md`: HTML/SVG conventions, Lavish loop, and export notes.
- `assets/html-figure-template/`: minimal two-panel HTML figure starter.

## Example Prompt

```text
Use $academic-figure-refiner to build a new multi-panel academic figure from this study description and dataset, then use Lavish for human-in-the-loop spacing, label, and panel-balance refinements.
```
