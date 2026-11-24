#!/usr/bin/env python3
"""Export an HTML academic figure to tightly cropped vector PDF and high-DPI PNG,
while auditing images, SVG text legibility, clipping, and label collisions.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
from pathlib import Path
from typing import Any

PX_PER_INCH = 96.0
MM_PER_INCH = 25.4
PT_PER_INCH = 72.0
PX_TO_MM = MM_PER_INCH / PX_PER_INCH
PX_TO_PT = PT_PER_INCH / PX_PER_INCH

SYSTEM_CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
)

AUDIT_JS = r"""
({ selector, minFontPt }) => {
  const pxToMm = 25.4 / 96.0;
  const pxToPt = 72.0 / 96.0;
  const target = document.querySelector(selector);
  if (!target) {
    return { error: `Selector not found: ${selector}` };
  }

  const figRect = target.getBoundingClientRect();
  if (figRect.width <= 0 || figRect.height <= 0) {
    return { error: `Target element has zero size: ${figRect.width}x${figRect.height}` };
  }

  const brokenImages = [];
  for (const img of target.querySelectorAll('img')) {
    if (!img.complete || img.naturalWidth === 0) {
      brokenImages.push({
        src: img.getAttribute('src') || '',
        alt: img.getAttribute('alt') || '',
      });
    }
  }

  const smallTexts = [];
  const overflowingTexts = [];
  const overlappingTexts = [];

  let minRenderedFontPt = null;
  let totalSvgTexts = 0;

  for (const svg of target.querySelectorAll('svg')) {
    const svgBoxes = [];
    for (const el of svg.querySelectorAll('text')) {
      const content = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!content) continue;

      const style = window.getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' || parseFloat(style.opacity) === 0) {
        continue;
      }

      const rect = el.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) continue;

      totalSvgTexts += 1;
      const fontSizePx = parseFloat(style.fontSize) || 0;
      const ctm = el.getScreenCTM();
      const scale = ctm ? Math.hypot(ctm.a, ctm.b) : 1.0;
      const effectivePt = fontSizePx * scale * pxToPt;

      if (minRenderedFontPt === null || effectivePt < minRenderedFontPt) {
        minRenderedFontPt = effectivePt;
      }

      if (effectivePt < minFontPt) {
        smallTexts.push({
          text: content.slice(0, 60),
          effectivePt: Number(effectivePt.toFixed(2)),
          cssFontSizePx: Number(fontSizePx.toFixed(2)),
          svgScale: Number(scale.toFixed(3)),
        });
      }

      const tolerance = 1.0;
      if (
        rect.left < figRect.left - tolerance ||
        rect.right > figRect.right + tolerance ||
        rect.top < figRect.top - tolerance ||
        rect.bottom > figRect.bottom + tolerance
      ) {
        overflowingTexts.push({
          text: content.slice(0, 60),
          rect: {
            left: Number(rect.left.toFixed(1)),
            top: Number(rect.top.toFixed(1)),
            right: Number(rect.right.toFixed(1)),
            bottom: Number(rect.bottom.toFixed(1)),
          },
          figureRect: {
            left: Number(figRect.left.toFixed(1)),
            top: Number(figRect.top.toFixed(1)),
            right: Number(figRect.right.toFixed(1)),
            bottom: Number(figRect.bottom.toFixed(1)),
          },
        });
      }

      svgBoxes.push({ text: content.slice(0, 60), rect });
    }

    for (let i = 0; i < svgBoxes.length; i++) {
      for (let j = i + 1; j < svgBoxes.length; j++) {
        const a = svgBoxes[i];
        const b = svgBoxes[j];
        const xOverlap = Math.max(0, Math.min(a.rect.right, b.rect.right) - Math.max(a.rect.left, b.rect.left));
        const yOverlap = Math.max(0, Math.min(a.rect.bottom, b.rect.bottom) - Math.max(a.rect.top, b.rect.top));
        if (xOverlap <= 0 || yOverlap <= 0) continue;

        const overlapArea = xOverlap * yOverlap;
        const minArea = Math.min(a.rect.width * a.rect.height, b.rect.width * b.rect.height);
        const ratio = minArea > 0 ? overlapArea / minArea : 0;
        if (ratio > 0.20) {
          overlappingTexts.push({
            textA: a.text,
            textB: b.text,
            overlapRatio: Number(ratio.toFixed(2)),
          });
        }
      }
    }
  }

  return {
    widthPx: Number(figRect.width.toFixed(2)),
    heightPx: Number(figRect.height.toFixed(2)),
    widthMm: Number((figRect.width * pxToMm).toFixed(2)),
    heightMm: Number((figRect.height * pxToMm).toFixed(2)),
    totalSvgTexts,
    minRenderedFontPt: minRenderedFontPt !== null ? Number(minRenderedFontPt.toFixed(2)) : null,
    brokenImages,
    smallTexts,
    overflowingTexts,
    overlappingTexts,
  };
}
"""

PREPARE_PDF_LAYOUT_JS = r"""
({ selector, padMm }) => {
  const target = document.querySelector(selector);
  if (!target) {
    return { error: `Selector not found: ${selector}` };
  }

  const style = document.createElement('style');
  style.id = '__academic_figure_pdf_crop__';
  style.textContent = `
    @page { margin: 0 !important; }
    html, body {
      margin: 0 !important;
      padding: 0 !important;
      background: #ffffff !important;
      min-height: 0 !important;
      height: auto !important;
    }
  `;
  document.head.appendChild(style);

  // Reset layout wrappers between body and target so the figure starts at top-left.
  let cur = target.parentElement;
  while (cur && cur !== document.documentElement) {
    cur.style.setProperty('margin', '0', 'important');
    cur.style.setProperty('padding', cur === document.body ? `${padMm}mm` : '0', 'important');
    cur.style.setProperty('min-height', '0', 'important');
    cur.style.setProperty('height', 'auto', 'important');
    cur.style.setProperty('display', 'block', 'important');
    cur.style.setProperty('overflow', 'visible', 'important');
    cur = cur.parentElement;
  }
  target.style.setProperty('margin', '0', 'important');

  const rect = target.getBoundingClientRect();
  const pxToMm = 25.4 / 96.0;
  return {
    widthMm: rect.width * pxToMm,
    heightMm: rect.height * pxToMm,
  };
}
"""


def find_system_chrome() -> str | None:
    """Return the first available local Chrome/Chromium executable path."""
    for name in ("google-chrome", "chromium", "chromium-browser"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    for path in SYSTEM_CHROME_CANDIDATES:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


def launch_browser(playwright: Any) -> tuple[Any, str]:
    """Launch Playwright Chromium, falling back to a local system Chrome binary."""
    launch_errors: list[str] = []
    try:
        browser = playwright.chromium.launch(headless=True)
        return browser, "playwright-chromium"
    except Exception as exc:  # noqa: BLE001
        launch_errors.append(f"playwright-chromium: {exc}")

    chrome_path = find_system_chrome()
    if chrome_path:
        try:
            browser = playwright.chromium.launch(executable_path=chrome_path, headless=True)
            return browser, f"system-chrome ({chrome_path})"
        except Exception as exc:  # noqa: BLE001
            launch_errors.append(f"system-chrome ({chrome_path}): {exc}")

    try:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        return browser, "channel-chrome"
    except Exception as exc:  # noqa: BLE001
        launch_errors.append(f"channel-chrome: {exc}")

    details = "\n  - ".join(launch_errors)
    raise RuntimeError(
        "Unable to launch a headless Chromium/Chrome browser.\n"
        f"Tried:\n  - {details}\n"
        "Install Playwright Chromium (`uv run playwright install chromium`) or ensure Google Chrome is installed."
    )


def wait_for_render_ready(page: Any) -> None:
    """Wait for fonts and images to settle before auditing or exporting."""
    page.evaluate(
        """async () => {
          if (document.fonts && document.fonts.ready) {
            await document.fonts.ready;
          }
          const imgs = Array.from(document.querySelectorAll('img'));
          await Promise.all(imgs.map((img) => {
            if (img.complete) return Promise.resolve();
            return new Promise((resolve) => {
              img.addEventListener('load', resolve, { once: true });
              img.addEventListener('error', resolve, { once: true });
            });
          }));
        }"""
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export an HTML academic figure to tightly cropped PDF/PNG and run layout audits."
    )
    parser.add_argument("html_path", type=Path, help="Path to the HTML figure file (e.g., index.html)")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory for exported files (default: <html_dir>/exports)",
    )
    parser.add_argument("--name", default="figure", help="Base filename without extension (default: figure)")
    parser.add_argument(
        "--selector",
        default=".paper-figure",
        help="CSS selector for the target figure container (default: .paper-figure)",
    )
    parser.add_argument("--dpi", type=float, default=300.0, help="Target DPI for PNG export (default: 300)")
    parser.add_argument(
        "--format",
        choices=("both", "pdf", "png"),
        default="both",
        help="Export format (default: both)",
    )
    parser.add_argument(
        "--pad-mm",
        type=float,
        default=2.0,
        help="Safety margin around target element in PDF output in mm (default: 2.0)",
    )
    parser.add_argument(
        "--min-font-pt",
        type=float,
        default=5.5,
        help="Minimum acceptable effective SVG font size in pt before warning (default: 5.5)",
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="Run layout and legibility audit without writing PDF or PNG files",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output")
    return parser


def run_export(args: argparse.Namespace) -> dict[str, Any]:
    html_path = args.html_path.expanduser().resolve()
    if not html_path.is_file():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    if args.dpi <= 0:
        raise ValueError(f"--dpi must be positive, got {args.dpi}")
    if args.pad_mm < 0:
        raise ValueError(f"--pad-mm must be non-negative, got {args.pad_mm}")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Python package 'playwright' is required in the active environment. "
            "Install it with `pip install playwright` (or `uv pip install playwright`) "
            "or run with your virtual environment's python."
        ) from exc

    out_dir = (args.out_dir.expanduser().resolve() if args.out_dir else html_path.parent / "exports")
    file_url = html_path.as_uri()
    exports: dict[str, str] = {}

    with sync_playwright() as p:
        browser, browser_source = launch_browser(p)
        try:
            # 1) Measure and audit at standard 96 dpi scale=1.0
            context = browser.new_context(viewport={"width": 1600, "height": 1200}, device_scale_factor=1.0)
            page = context.new_page()
            page.goto(file_url, wait_until="load")
            wait_for_render_ready(page)

            audit = page.evaluate(AUDIT_JS, {"selector": args.selector, "minFontPt": args.min_font_pt})
            if "error" in audit:
                raise RuntimeError(audit["error"])

            fig_w_px = float(audit["widthPx"])
            fig_h_px = float(audit["heightPx"])
            vp_w = max(1600, math.ceil(fig_w_px) + 200)
            vp_h = max(1200, math.ceil(fig_h_px) + 200)

            if not args.audit_only:
                out_dir.mkdir(parents=True, exist_ok=True)

                # 2) Export tightly cropped vector PDF (in print media mode)
                if args.format in ("both", "pdf"):
                    page.emulate_media(media="print")
                    pdf_dims = page.evaluate(
                        PREPARE_PDF_LAYOUT_JS,
                        {"selector": args.selector, "padMm": args.pad_mm},
                    )
                    if "error" in pdf_dims:
                        raise RuntimeError(pdf_dims["error"])

                    total_w_mm = float(pdf_dims["widthMm"]) + 2.0 * args.pad_mm
                    total_h_mm = float(pdf_dims["heightMm"]) + 2.0 * args.pad_mm
                    pdf_path = out_dir / f"{args.name}.pdf"
                    page.pdf(
                        path=str(pdf_path),
                        width=f"{total_w_mm:.2f}mm",
                        height=f"{total_h_mm:.2f}mm",
                        margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
                        print_background=True,
                        prefer_css_page_size=False,
                    )
                    exports["pdf"] = str(pdf_path)

            context.close()

            # 3) Export high-DPI PNG using dedicated device_scale_factor context
            if not args.audit_only and args.format in ("both", "png"):
                scale = args.dpi / PX_PER_INCH
                png_context = browser.new_context(
                    viewport={"width": vp_w, "height": vp_h},
                    device_scale_factor=scale,
                )
                png_page = png_context.new_page()
                png_page.goto(file_url, wait_until="load")
                wait_for_render_ready(png_page)
                png_path = out_dir / f"{args.name}.png"
                png_page.locator(args.selector).first.screenshot(path=str(png_path), omit_background=False)
                exports["png"] = str(png_path)
                png_context.close()
        finally:
            browser.close()

    warnings: list[str] = []
    if audit["brokenImages"]:
        warnings.append(f"{len(audit['brokenImages'])} broken <img> element(s)")
    if audit["smallTexts"]:
        warnings.append(
            f"{len(audit['smallTexts'])} SVG text element(s) below {args.min_font_pt} pt "
            f"(min={audit['minRenderedFontPt']} pt)"
        )
    if audit["overflowingTexts"]:
        warnings.append(f"{len(audit['overflowingTexts'])} SVG text element(s) overflow {args.selector}")
    if audit["overlappingTexts"]:
        warnings.append(f"{len(audit['overlappingTexts'])} overlapping SVG text pair(s)")

    return {
        "html": str(html_path),
        "selector": args.selector,
        "browser": browser_source,
        "dpi": args.dpi,
        "dimensions": {
            "widthPx": audit["widthPx"],
            "heightPx": audit["heightPx"],
            "widthMm": audit["widthMm"],
            "heightMm": audit["heightMm"],
        },
        "audit": audit,
        "warnings": warnings,
        "exports": exports,
    }


def print_human_summary(result: dict[str, Any]) -> None:
    dims = result["dimensions"]
    audit = result["audit"]
    print(f"HTML:       {result['html']}")
    print(f"Browser:    {result['browser']}")
    print(
        f"Dimensions: {dims['widthMm']} mm x {dims['heightMm']} mm "
        f"({dims['widthPx']} px x {dims['heightPx']} px @ 96 dpi)"
    )
    min_pt = audit["minRenderedFontPt"]
    min_pt_str = f"{min_pt} pt" if min_pt is not None else "n/a"
    print(
        f"SVG Audit:  {audit['totalSvgTexts']} text node(s), min font={min_pt_str}, "
        f"broken_imgs={len(audit['brokenImages'])}, small_texts={len(audit['smallTexts'])}, "
        f"overflows={len(audit['overflowingTexts'])}, overlaps={len(audit['overlappingTexts'])}"
    )
    if result["warnings"]:
        print("Warnings:")
        for w in result["warnings"]:
            print(f"  - {w}")
        if audit["brokenImages"]:
            print(f"  brokenImages: {json.dumps(audit['brokenImages'], ensure_ascii=False)}")
        if audit["smallTexts"]:
            print(f"  smallTexts:   {json.dumps(audit['smallTexts'], ensure_ascii=False)}")
        if audit["overflowingTexts"]:
            print(f"  overflows:    {json.dumps(audit['overflowingTexts'], ensure_ascii=False)}")
        if audit["overlappingTexts"]:
            print(f"  overlaps:     {json.dumps(audit['overlappingTexts'], ensure_ascii=False)}")
    else:
        print("Audit:      PASS (no broken images, small text, clipping, or overlaps)")

    if result["exports"]:
        print("Exports:")
        for fmt, path in result["exports"].items():
            size_kb = Path(path).stat().st_size / 1024.0
            print(f"  - {fmt.upper()}: {path} ({size_kb:.1f} KB)")


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = run_export(args)
    except Exception as exc:  # noqa: BLE001
        if args.json:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
