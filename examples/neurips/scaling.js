const budgets = [5, 10, 20, 40, 80, 160];
const methods = [
  {
    name: 'Rerank', color: '#b84b16',
    runsByBudget: [
      [43, 46, 51, 51, 45], [54, 55, 59, 62, 60], [67, 62, 74, 69, 70],
      [75, 78, 78, 83, 78], [81, 84, 87, 91, 87], [86, 88, 93, 91, 92]
    ]
  },
  {
    name: 'Dense', color: '#0072b2', dash: '5 3',
    runsByBudget: [
      [43, 46, 51, 51, 45], [47, 50, 52, 57, 53], [53, 55, 57, 62, 63],
      [59, 66, 65, 69, 69], [66, 68, 72, 74, 72], [69, 71, 78, 76, 75]
    ]
  }
];

const chart = document.querySelector('#scaling');
const scale = plotFrame(chart,
  { left: 36, right: 226, top: 26, bottom: 141, xMin: 5, xMax: 160, yMin: 35, yMax: 98, xTransform: Math.log2 },
  budgets.map(value => [value, value]),
  [40, 50, 60, 70, 80, 90].map(value => [value, value]),
  'Candidate budget (log₂ scale)', 'Recall@5 (%)');

for (const [index, method] of methods.entries()) {
  legendLine(chart, 50 + index * 82, 12, method.name, method.color, method.dash);
  const data = method.runsByBudget.map((runs, i) => {
    const mean = runs.reduce((sum, value) => sum + value, 0) / runs.length;
    const sumSquares = runs.reduce((sum, value) => sum + (value - mean) ** 2, 0);
    return { budget: budgets[i], mean, sd: Math.sqrt(sumSquares / (runs.length - 1)) };
  });
  const upper = data.map(({ budget, mean, sd }) => [scale.x(budget), scale.y(mean + sd)]);
  const lower = data.map(({ budget, mean, sd }) => [scale.x(budget), scale.y(mean - sd)]).reverse();
  draw(chart, 'polygon', { points: upper.concat(lower).map(pair => pair.join(',')).join(' '),
    fill: method.color, 'fill-opacity': 0.15 });
  plotSeries(chart, scale, data.map(({ budget, mean }) => [budget, mean]), { ...method, markers: true });
}
