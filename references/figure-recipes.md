# Figure Recipes

Use this reference after classifying the figure type.

## Multi-Panel Figures

- Define the figure claim, panel list, target width (single/1.5/double column), and required source data or evidence before drawing.
- Size each panel's SVG `viewBox` to match its actual CSS grid column width at `96 dpi` (`1:1` coordinate mapping) so typography stays consistent across panels.
- Define a stable grid and panel labels (`A`, `B`, `C`, ...) before styling details.
- Make panel labels consistent in size, weight, and upper-left offset.
- Align internal axes, image bounds, captions, and legends across adjacent panels.
- Keep repeated variables, methods, groups, and conditions the exact same color and line style across all panels.

## Mechanism Or Conceptual Diagrams

- List the entities, relationships, directionality, and claims that the diagram must communicate before sketching SVG geometry.
- Use SVG shapes, paths, and labels rather than flattened images.
- Use a restrained palette with neutral structural grays and one or two accent colors.
- Prefer clean orthogonal/curved connectors, consistent arrowheads, and grouped modules over decorative illustration.
- Keep causal or temporal direction obvious (left-to-right or top-to-bottom).
- Avoid adding mechanisms or modules not present in the reference or study description.

## Model Architecture, System & Agent Pipelines (AI / ML)

- Separate **data flow** (solid arrows), **gradient/feedback/control flow** (dashed or colored arrows), and **optional/skip paths** (light gray or annotated).
- Distinguish **trainable modules**, **frozen/pretrained backbones**, and **external tools/environments** with consistent fill tints or subtle dashed outlines rather than decorative gradients.
- Annotate key tensor dimensions, token budgets, or stage I/O concisely at connectors (`B × L × d`, `k = 8`, `T steps`).
- Group repeated layers or multi-agent loops into cleanly labeled sub-blocks with subtle neutral backgrounds (`#F3F5F6`), avoiding nested app-UI cards or heavy shadows.
- Place short legend chips directly inside or below the diagram explaining arrow/box encodings.

## Behavioral Task Flows

- Define trial phases, timing, conditions, stimuli, response windows, and feedback before drawing.
- Represent time explicitly with a clear horizontal or vertical timeline axis.
- Preserve stimulus timing, response windows, trial phases, and condition labels verbatim.
- Use repeated visual grammar for fixation, stimulus, delay, response, feedback, and ITI/rest.
- Keep task screenshots or stimulus examples as raster assets in `assets/` and surround them with vector annotations.
- Use concise labels; keep verbose instructions in the paper caption rather than inside boxes.

## Data Charts

- **Do not hand-calculate SVG coordinates** for non-trivial statistical plots (error bars, confidence bands, KDEs/violins, dense scatter plots, regression curves). Generate them programmatically from `data.csv`/`data.json`:
  - **Preferred for scientific/ML charts**: Python `matplotlib`/`seaborn` configured with `rcParams['svg.fonttype'] = 'none'`, sized to the exact target column width in inches (`width_mm / 25.4`), exported as transparent SVG, and placed into the HTML grid.
  - **Alternative**: inline deterministic JS inside `index.html` reading `data.csv`/`data.json` to render exact SVG paths.
  - Hand-coded SVG charts are appropriate only for very simple 2–5 bar summaries when verified directly against exact numbers.
- Preserve axes, scales, units, sample sizes (`n = ...`), and statistical annotations (`p`, `*`, CI definitions).
- Avoid chartjunk, 3D effects, heavy shadows, decorative gradients, and unnecessary top/right spines.
- Prefer direct curve/bar labels when space permits; otherwise keep legends compact and aligned.
- If reconstructing values from a screenshot because raw data are unavailable, mark extracted values as approximate.

## Training, Scaling, Ablation Curves & Pareto Trade-offs (AI / ML)

- **Baseline vs. Proposed Hierarchy**: render baseline/reference curves in muted neutral gray or dashed strokes (`#5F6368`, `#8C969E`) and reserve bold solid Okabe-Ito accents (`1.2–1.5 pt`) for the proposed method and key ablations.
- **Uncertainty & Seeds**: display `mean ± SD`, `SE`, or min-max shaded bands with low opacity (`0.15–0.22`) generated from the actual seed runs via plotting script, and state the band definition in the legend or note.
- **Scaling Laws & Log Axes**: verify tick formatting (`10^7`, `10^8` or `10M`, `100M`), minor ticks if helpful, and clearly mark power-law fits vs. empirical points.
- **Pareto / Efficiency Plots**: draw the Pareto frontier explicitly (thin dashed or step line), highlight the favorable corner (e.g., arrow or subtle label `"Better"`), and annotate parameter/FLOPs/latency budgets directly near key points without overlapping markers.
- **Ablation Bar / Dot Plots**: prefer horizontal dot-and-error-bar (Cleveland dot) or sorted bar charts with a dashed baseline reference line when comparing 5+ variants with close metric scores.

## Correlation Matrices And Heatmaps

- Generate dense matrices (`> 5×5`) programmatically from source numeric arrays (`matplotlib`/`seaborn` to SVG with `svg.fonttype = 'none'`, or JS from `data.json`) rather than typing individual `<rect>` cells manually.
- Preserve row/column ordering, clustering hierarchy, labels, value scale, missing-value masks, and color semantics.
- Use a perceptually uniform sequential palette (e.g., `viridis`, `cividis`, `rocket_r`) for unsigned values and a color-blind-safe diverging palette (e.g., `RdBu_r` or `coolwarm` with balanced midpoint) for signed correlations.
- Include a readable color bar with explicit endpoints, midpoint (`0` when diverging), and units/metric name (`Pearson r`, `Cosine sim.`).
- Avoid over-saturated colors that mask midrange differences; rotate tick labels cleanly (`35°–45°`) only when needed to avoid collisions.

## Mathematical Notation & Greek Symbols In SVG

- Avoid leaving raw LaTeX syntax (`$\alpha$`, `\mathcal{L}`) in SVG `<text>` unless compiled offline into SVG paths/glyphs; browser SVG does not run LaTeX natively.
- Use clean Unicode math/Greek characters (`α, β, γ, θ, λ, μ, σ, τ, Σ, Δ, ∈, ≈, ≤, ≥, ×, ±, →`) alongside standard ASCII variables.
- Format subscripts and superscripts reliably across SVG renderers and PDF export using `<tspan dy="..." font-size="75%">...</tspan>` and resetting `dy` on the following `<tspan>`:
  ```xml
  <text x="40" y="24">L<tspan dy="3" font-size="75%">KL</tspan><tspan dy="-3"> (θ)</tspan></text>
  ```
- Test exported PDF/PNG to verify that fallback math glyphs (e.g., `Σ`, `∈`) render cleanly in the chosen sans-serif font without clipping or vertical drift.

## Brain, MRI, fMRI, And Imaging Panels

- Collect source images, orientation labels (`L/R`, `A/P`, `S/I`), MNI/slice coordinates, color bars, ROI labels, and statistical threshold notes before layout.
- Preserve raw image evidence and orientation labels untouched.
- Use vector SVG overlays for arrows, outlines, ROI callouts, and scale/color bars.
- Do not alter activation maps, lesions, structures, or contrast/brightness in ways that change interpretation.
- Keep crop, scale, and window/level handling consistent across slices or subjects.

## Microscopy, Histology, Gel, And Other Image Panels

- Collect source images, physical scale calibration, treatment/group labels, and approved annotation needs before layout.
- Preserve raw or source image files in `assets/` without local retouching or selective cleanup.
- Use separate SVG overlay layers for labels, arrows, outlines, inset zoom boxes, and labeled scale bars.
- Keep scale bars consistent in physical units and clearly legible over dark/light backgrounds (add a subtle dark/light halo or backing pill only around the scale bar/label if needed for contrast).
- Use panel borders only when needed to separate adjacent images cleanly.
