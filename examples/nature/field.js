// Synthetic field on a 240 × 120 km domain. Transects sample this same grid.
const columns = 80;
const rows = 48;
const map = { left: 39, top: 8, width: 352, height: 154 };
const cellW = map.width / columns;
const cellH = map.height / rows;
const transects = [
  { name: 'North', row: 11, color: '#0072b2' },
  { name: 'South', row: 33, color: '#b84b16', dash: '5 3' }
];
const palette = [
  [18, 48, 91], [33, 85, 125], [38, 122, 141], [54, 159, 139],
  [119, 190, 111], [188, 213, 87], [248, 230, 116]
];

function colorAt(fraction) {
  const p = Math.max(0, Math.min(fraction, 1)) * (palette.length - 1);
  const index = Math.min(palette.length - 2, Math.floor(p));
  const f = p - index;
  return `rgb(${palette[index].map((value, c) =>
    Math.round(value + (palette[index + 1][c] - value) * f)).join(',')})`;
}

function temperature(x, y) {
  const coast = 0.23 + 0.055 * Math.sin(7.8 * y) + 0.022 * Math.sin(22 * y + 0.5);
  if (x < coast) return null;
  const plume = 0.39 + 0.38 * y + 0.095 * Math.sin(9.8 * y + 0.7);
  const plumeDistance = (x - plume) / (0.102 + 0.045 * y);
  const warmCore = 9.2 * Math.exp(-(plumeDistance ** 2)) * (0.46 + 0.54 * Math.sin(Math.PI * y));
  const coolEdge = 1.6 * Math.cos(6.4 * y + 4.2 * x);
  const texture = 0.46 * Math.sin(25 * x - 15 * y) * Math.cos(14 * x + 29 * y);
  return 17.3 + 2.8 * x + warmCore + coolEdge + texture;
}

const field = Array.from({ length: rows }, (_, row) =>
  Array.from({ length: columns }, (_, col) => temperature((col + 0.5) / columns, (row + 0.5) / rows)));
const fieldSvg = document.querySelector('#field');
const cells = draw(fieldSvg, 'g', { transform: `translate(${map.left} ${map.top}) scale(${cellW} ${cellH})` });
const colorPaths = new Map();
for (const [row, values] of field.entries()) {
  for (const [col, value] of values.entries()) {
    const fill = value === null ? '#e6e7e3' : colorAt(Math.round((value - 16) * 4) / 64);
    const cell = `M${col} ${row}h1v1h-1Z`;
    colorPaths.set(fill, (colorPaths.get(fill) ?? '') + cell);
  }
}
for (const [fill, d] of colorPaths) draw(cells, 'path', { d, fill, 'shape-rendering': 'crispEdges' });
draw(fieldSvg, 'rect', { x: map.left, y: map.top, width: map.width, height: map.height,
  fill: 'none', stroke: '#56677b', 'stroke-width': '0.55pt' });

for (const transect of transects) {
  const y = map.top + (transect.row + 0.5) * cellH;
  const first = field[transect.row].findIndex(value => value !== null);
  const x1 = map.left + (first + 0.5) * cellW;
  const x2 = map.left + (columns - 0.5) * cellW;
  draw(fieldSvg, 'line', { x1, x2, y1: y, y2: y, stroke: '#fff',
    'stroke-width': '1pt', 'stroke-dasharray': transect.dash ?? 'none' });
  label(fieldSvg, 366, y - 6, transect.name[0], 'image-annotation', 'middle');
}

for (const fraction of [0, 0.25, 0.5, 0.75, 1]) {
  const x = map.left + fraction * map.width;
  draw(fieldSvg, 'line', { x1: x, x2: x, y1: 162, y2: 165, class: 'axis-line' });
  label(fieldSvg, x, 177, fraction * 240, 'tick-label', 'middle');
}
for (const fraction of [0, 0.5, 1]) {
  const y = 162 - fraction * map.height;
  label(fieldSvg, 33, y + 3, fraction * 120, 'tick-label', 'end');
}
label(fieldSvg, 215, 192, 'Domain distance (km)', 'axis-title', 'middle');
label(fieldSvg, 9, 85, 'Northing (km)', 'axis-title', 'middle')
  .setAttribute('transform', 'rotate(-90 9 85)');
const gradient = draw(draw(fieldSvg, 'defs', {}), 'linearGradient', { id: 'temperature-gradient' });
for (const [index, color] of palette.entries()) {
  draw(gradient, 'stop', { offset: index / (palette.length - 1), 'stop-color': `rgb(${color})` });
}
draw(fieldSvg, 'rect', { x: 126, y: 204, width: 159, height: 8, fill: 'url(#temperature-gradient)' });
label(fieldSvg, 121, 211, '16', 'tick-label', 'end');
label(fieldSvg, 290, 211, '32 °C', 'tick-label');

const transectSvg = document.querySelector('#transects');
const axis = plotFrame(transectSvg,
  { left: 40, right: 250, top: 31, bottom: 162, xMin: 0, xMax: 240, yMin: 16, yMax: 32 },
  [0, 60, 120, 180, 240].map(value => [value, value]),
  [16, 20, 24, 28, 32].map(value => [value, value]),
  'Domain distance (km)', 'Temperature (°C)');
for (const [index, transect] of transects.entries()) {
  legendLine(transectSvg, 66 + index * 80, 15, transect.name, transect.color, transect.dash);
  const samples = field[transect.row]
    .map((value, col) => [(col + 0.5) / columns * 240, value])
    .filter(([, value]) => value !== null);
  plotSeries(transectSvg, axis, samples, transect);
}
