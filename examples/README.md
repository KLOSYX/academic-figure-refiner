# Figure demos

Open any `index.html` directly in a browser. The pages load their data, styles, and images from this repository and work offline.

| Figure | Target content width | Source of plotted values |
| --- | ---: | --- |
| [Coastal temperature field](nature/index.html) | 183 mm | [Deterministic field and transect sampling](nature/field.js) |
| [Two-stage retrieval](neurips/index.html) | 139.7 mm | [Illustrative runs, sample means, and sample standard deviations](neurips/scaling.js) |
| [Simulated fluorescence](cell/index.html) | 174 mm | [Generated phantom, exact inset crop, and sampled line profiles](cell/build_phantom.py) |

The widths follow the [Nature research figure guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/), [NeurIPS formatting instructions](https://media.neurips.cc/Conferences/NeurIPS2023/Styles/neurips_2023.pdf), and [Cell Press figure guidelines](https://www.cell.com/information-for-authors/figure-guidelines). The charts and imagery are simulations for demonstrating the workflow.

From the repository root, with the exporter dependencies installed:

```bash
python scripts/export_figure.py examples/nature/index.html --pad-mm 0.5 --dpi 300
python scripts/export_figure.py examples/neurips/index.html --pad-mm 0.5 --dpi 300
python scripts/export_figure.py examples/cell/index.html --pad-mm 0.5 --dpi 600
python scripts/export_figure.py examples/cover.html --selector .cover --format png --dpi 120 --name readme-header --out-dir assets
```

Each PDF includes 0.5 mm of safety padding on all sides. The [cover source](cover.html) uses the three exported PNGs. To regenerate the Cell Press demo's source rasters and profile samples, install Pillow, run `python examples/cell/build_phantom.py`, and re-run the Cell and cover exports.
