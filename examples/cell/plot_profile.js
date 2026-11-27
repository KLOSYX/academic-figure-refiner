const profile = document.querySelector('#profile');
const axes = plotFrame(profile,
  { left: 38, right: 175, top: 25, bottom: 139, xMin: 0, xMax: 110, yMin: 0, yMax: 1 },
  [[0, 0], [25, 25], [50, 50], [75, 75], [100, 100]],
  [[0, '0'], [0.25, '0.25'], [0.5, '0.5'], [0.75, '0.75'], [1, '1']],
  'Distance (μm)', 'Normalized intensity');

legendLine(profile, 36, 11, 'Cyan', '#007e69');
legendLine(profile, 98, 11, 'Magenta', '#a23784', '5 3');
plotSeries(profile, axes, phantomProfile.map(([distance, cyan]) => [distance, cyan]),
  { color: '#007e69' });
plotSeries(profile, axes, phantomProfile.map(([distance, , magenta]) => [distance, magenta]),
  { color: '#a23784', dash: '5 3' });
