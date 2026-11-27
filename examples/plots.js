const svgSpace = 'http://www.w3.org/2000/svg';

function draw(parent, tag, attributes, content) {
  const element = document.createElementNS(svgSpace, tag);
  for (const [name, value] of Object.entries(attributes)) element.setAttribute(name, value);
  if (content !== undefined) element.textContent = content;
  parent.append(element);
  return element;
}

function label(parent, x, y, content, className, anchor = 'start') {
  return draw(parent, 'text', { x, y, class: className, 'text-anchor': anchor }, content);
}

function plotFrame(svg, bounds, xTicks, yTicks, xTitle, yTitle) {
  const { left, right, top, bottom, xMin, xMax, yMin, yMax, xTransform = x => x } = bounds;
  const x0 = xTransform(xMin);
  const xSpan = xTransform(xMax) - x0;
  const x = value => left + (xTransform(value) - x0) / xSpan * (right - left);
  const y = value => bottom - (value - yMin) / (yMax - yMin) * (bottom - top);

  for (const [value, caption] of yTicks) {
    draw(svg, 'line', { x1: left - 3, x2: right, y1: y(value), y2: y(value), class: 'grid-line' });
    label(svg, left - 6, y(value) + 3, caption, 'tick-label', 'end');
  }
  for (const [value, caption] of xTicks) {
    draw(svg, 'line', { x1: x(value), x2: x(value), y1: bottom, y2: bottom + 3, class: 'axis-line' });
    label(svg, x(value), bottom + 15, caption, 'tick-label', 'middle');
  }
  draw(svg, 'path', { d: `M${left} ${top}V${bottom}H${right}`, class: 'axis-line' });
  label(svg, (left + right) / 2, bottom + 31, xTitle, 'axis-title', 'middle');
  label(svg, 9, (top + bottom) / 2, yTitle, 'axis-title', 'middle')
    .setAttribute('transform', `rotate(-90 9 ${(top + bottom) / 2})`);
  return { x, y };
}

function plotSeries(svg, scale, points, { color, dash, markers = false }) {
  const coords = points.map(([x, y]) => `${scale.x(x).toFixed(2)},${scale.y(y).toFixed(2)}`);
  const style = { points: coords.join(' '), fill: 'none', stroke: color, 'stroke-width': '1.25pt',
    'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
  if (dash) style['stroke-dasharray'] = dash;
  draw(svg, 'polyline', style);
  if (markers) {
    for (const [x, y] of points) {
      draw(svg, 'circle', { cx: scale.x(x), cy: scale.y(y), r: 2.3, fill: 'white', stroke: color });
    }
  }
}

function legendLine(svg, x, y, caption, color, dash) {
  const style = { x1: x, x2: x + 15, y1: y - 3, y2: y - 3, stroke: color, 'stroke-width': '1.25pt' };
  if (dash) style['stroke-dasharray'] = dash;
  draw(svg, 'line', style);
  label(svg, x + 20, y, caption, 'tick-label');
}
