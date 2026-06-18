# HTML Figure Workflow

Use this reference when building first-pass editable HTML/CSS/SVG figure projects and refining them through Lavish.

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

Lavish is the recommended human-in-the-loop fine-tuning step after the first complete HTML figure draft exists. Use it when the figure is structurally correct but needs human-guided polish: tighter spacing, better alignment, label wording, panel balance, arrow placement, color consistency, local overlap fixes, visual hierarchy adjustments, or small visual corrections that are hard to describe without pointing at the artifact.

1. Finish a coherent first HTML draft before starting Lavish. Do not use Lavish to replace scientific validation or data checking.
2. From the directory containing the figure project, run:

```bash
npx -y lavish-axi index.html
```

3. The command returns a local session URL such as `http://127.0.0.1:4387/session/...`, the resolved file path, and a `next_step` telling the agent to poll. The same HTML file may resume the same session.
4. Ask the user to annotate elements, selected text, or layout regions directly in the browser.
5. Poll for feedback when running an interactive agent loop:

```bash
npx -y lavish-axi poll index.html
```

6. `poll` long-polls and normally stays silent until the user sends feedback or ends the session. Do not treat silence as failure.
7. Revise `index.html`, `styles.css`, SVG layers, and local assets based on the precise feedback.
8. After applying feedback, send a short response back into Lavish and wait for the next review pass:

```bash
npx -y lavish-axi poll index.html --agent-reply "Updated the spacing and label alignment; please review the revised figure."
```

9. Repeat until layout warnings and user review feedback are resolved.

Use relative asset paths. Avoid root-prefixed paths such as `/assets/image.png`, which may fail in local artifact routes.

Recommended loop:

```text
build first HTML draft
  -> launch Lavish
  -> collect precise human feedback
  -> patch HTML/CSS/SVG
  -> re-render and repeat
  -> export PDF/PNG
```

## Lavish CLI Notes And Pitfalls

These notes come from a direct CLI run against the bundled HTML template.

- `npx -y lavish-axi --help` prints playbook guidance and confirms the intended workflow: create the HTML artifact first, then run `lavish-axi <html-file>`, then `lavish-axi poll <html-file>`.
- Lavish serves the HTML through a local Express server, observed on port `4387`. Treat the returned URL as the review surface, not the final artifact URL.
- Keep every local dependency reachable from the HTML file with relative paths. CSS, images, fonts, and scripts should live next to the HTML file or in relative subdirectories such as `assets/`. Do not use `/assets/...`.
- `poll` is intentionally blocking. In normal use, do not add `--timeout-ms`; it is for tests/debugging and may not behave like an ordinary short timeout in all harnesses.
- If the execution environment kills or times out a foreground poll, rerun `lavish-axi poll <html-file>`. Lavish reports that queued feedback is not lost.
- If `poll` returns `SERVER_ERROR` or says the server did not start, rerun `lavish-axi <html-file>` and then poll again.
- If `lavish-axi server --port 4387` reports `EADDRINUSE`, check for a stale node process:

```bash
lsof -nP -iTCP:4387 -sTCP:LISTEN
```

Then stop the stale process if it belongs to the current Lavish test/session.

- `lavish-axi stop` may report `not-running` even when a node process is still listening on the port. Trust `lsof` when debugging port conflicts.
- `lavish-axi end <html-file>` can fail with the same server-start error when no server is reachable. Prefer ending from the active session, or restart the session and then end.
- Lavish does not inject a design system. The HTML should remain portable and render correctly when opened directly without Lavish. For this skill, prefer the academic CSS/template rather than Lavish's generic Tailwind/DaisyUI suggestion unless the user explicitly asks for a different design system.
- The template includes `<meta name="lavish-live-reload" content="root" />` so Lavish can reload changes during refinement.

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
