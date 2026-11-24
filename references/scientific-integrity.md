# Scientific Integrity Rules

Use this reference before building, modifying, or rebuilding any figure with scientific meaning.

## Non-Negotiable Rule

Improve clarity and presentation without changing scientific meaning. If a visual change could alter interpretation, ask for author confirmation or source data before proceeding.

## Never Invent Or Alter

- Data values, trends, distributions, outliers, or error bars
- Statistical significance, p-values, brackets, or confidence intervals
- Axis limits, scales, labels, units, or transformations
- Group names, condition names, stimuli, task timing, or sample descriptions
- Brain regions, activation maps, lesion boundaries, microscopy structures, bands, cells, or other empirical evidence
- Scale bars, image orientation, slice labels, anatomical labels, or acquisition metadata

## Data Plotting Integrity

- **Do not hand-calculate SVG coordinates** for non-trivial statistical charts (error bands, KDEs, violins, dense scatter plots, regression curves, or heatmaps).
- Always bind empirical data charts to verified source files (`data.csv`, `data.json`) via a reproducible script (such as Python `matplotlib`/`seaborn` exporting editable SVG, or deterministic JavaScript reading the data file).
- When illustrating a qualitative hypothesis or schematic trend without numeric data, label axes or notes explicitly as schematic/conceptual rather than disguising illustrative curves as empirical results.

## When To Ask For Data

Ask for source data or tables when:

- Rebuilding a chart from a screenshot
- Redrawing correlations, heatmaps, distributions, or time series
- Axis ticks are unreadable or values are ambiguous
- The user asks to make data "smoother," "cleaner," "more significant," or "more convincing"
- Visual approximation would affect the scientific conclusion

If the user only has a screenshot, you may create a visual approximation for layout planning, but explicitly label extracted numbers/curves as approximate and requiring author verification.

## Raster Evidence

- Preserve original raster files separately in `assets/`.
- Apply only global, consistent, explainable adjustments unless the user provides an approved protocol.
- Do not remove artifacts, background, cells, bands, activations, tissue boundaries, or other content that could be evidence.
- Put labels, arrows, outlines, masks, and scale bars on separate SVG overlay layers when possible.
- Keep before/after provenance clear when image enhancement is performed.

## Generative Image Editing Boundary

Use generative image editing only for non-evidence elements:

- stylized schematic backgrounds
- conceptual icons
- illustrative but non-data scene elements
- visual polish for non-scientific decoration explicitly requested by the user

Do not use generative editing to repair or fabricate scientific images, add missing data, remove inconvenient structures, or change the apparent result.

## Reporting Back

When delivering a refined figure, state:

- what was generated from source data vs. redrawn or restyled
- what original evidence was preserved
- whether any data were approximated from a reference image
- what must be checked by the author before submission
