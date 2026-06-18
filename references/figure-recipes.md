# Figure Recipes

Use this reference after classifying the figure type.

## Multi-Panel Figures

- Establish the target width first: single-column, double-column, or full-page.
- Define a stable grid and panel labels before styling details.
- Make panel labels consistent in size, weight, and position.
- Align internal axes, image bounds, captions, and legends across panels.
- Keep repeated variables, groups, and conditions visually consistent across panels.

## Mechanism Or Conceptual Diagrams

- Use SVG shapes, paths, and labels rather than flattened images.
- Use a restrained palette with one or two accent colors.
- Prefer simple arrows and grouped modules over decorative illustration.
- Keep causal or temporal direction obvious.
- Avoid adding mechanisms not present in the reference or user description.

## Behavioral Task Flows

- Represent time explicitly with a horizontal or vertical sequence.
- Preserve stimulus timing, response windows, trial phases, and condition labels.
- Use repeated visual grammar for stimuli, fixation, response, feedback, and rest.
- Keep task screenshots or stimulus examples as assets and surround them with vector annotations.
- Use concise labels; put long descriptions in the caption, not inside the figure.

## Data Charts

- Prefer rebuilding from source data in CSV/JSON.
- Preserve axes, scales, units, group labels, sample sizes, and statistical annotations.
- Avoid chartjunk, 3D effects, heavy shadows, decorative gradients, and unneeded borders.
- Use color and direct labels consistently across related panels.
- If redrawing from a screenshot, mark extracted values as approximate.

## Correlation Matrices And Heatmaps

- Preserve row/column order, labels, scale, and color meaning.
- Use a perceptually coherent diverging palette for signed values.
- Include a readable color bar with endpoints and units or correlation coefficient label.
- Avoid over-saturated colors that obscure midrange values.
- Rotate or abbreviate labels only if readability improves.

## Brain, MRI, fMRI, And Imaging Panels

- Preserve source image evidence and orientation labels.
- Keep anatomical labels, slice coordinates, scale bars, color bars, and threshold notes intact.
- Use vector overlays for arrows, outlines, ROI labels, and callouts.
- Do not alter activation, lesions, structures, or contrast in a way that changes interpretation.
- If using multiple slices or subjects, keep crop, scale, and brightness handling consistent.

## Microscopy, Histology, Gel, And Other Image Panels

- Preserve raw or source image files.
- Use separate overlays for labels, arrows, outlines, and scale bars.
- Keep scale bars consistent and labeled.
- Avoid local retouching or selective cleanup.
- Use panel borders only when they help distinguish adjacent images.
