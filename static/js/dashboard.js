document.addEventListener('DOMContentLoaded', async () => {
  const res = await fetch('/api/links');
  const links = await res.json();
  if (!links.length) return;

  const allByDay = {};
  const allReferrers = {};

  for (const link of links) {
    const ar = await fetch(`/api/links/${link.short_code}/analytics`);
    const data = await ar.json();
    data.by_day.forEach(d => { allByDay[d.date] = (allByDay[d.date] || 0) + d.count; });
    data.top_referrers.forEach(r => { allReferrers[r.name] = (allReferrers[r.name] || 0) + r.count; });
  }

  const days = Object.keys(allByDay).sort();
  new Chart(document.getElementById('clicksChart'), {
    type: 'line',
    data: {
      labels: days.map(d => d.slice(5)),
      datasets: [{
        label: 'Clicks',
        data: days.map(d => allByDay[d]),
        borderColor: '#1677ff',
        backgroundColor: 'rgba(22, 119, 255, 0.12)',
        fill: true, tension: 0.35, pointRadius: 3, pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  });

  const refEntries = Object.entries(allReferrers).sort((a, b) => b[1] - a[1]).slice(0, 5);
  new Chart(document.getElementById('referrersChart'), {
    type: 'bar',
    data: {
      labels: refEntries.map(e => e[0]),
      datasets: [{ data: refEntries.map(e => e[1]), backgroundColor: '#1677ff', borderRadius: 6 }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  });
});
