const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/ball2_engine.js' });
  const r = await p.evaluate(() => { const axe = [], grow = [];
    for (let seed = 1; seed <= 40; seed++) { const s = new AxeSim({ seed }); const marks = [];
      while (s.state === 'run' && s.t < 26) { s.stepFrame(); if (s.frame % 300 === 0) marks.push(s.count); }
      axe.push({ seed, end: +(s.finaleT || 0).toFixed(1), final: s.finalCount, marks: marks.join(',') }); }
    for (let seed = 1; seed <= 120; seed++) { const s = new GrowSim({ seed }); while (s.state === 'run' && s.t < 30) s.stepFrame();
      grow.push({ seed, end: +(s.finaleT || 0).toFixed(1), lc: s.leadChanges, win: s.winner, natural: s.balls.length === 1 || true }); }
    return { axe, grow }; });
  const ax = r.axe.filter(o => o.final >= 60 && o.end >= 14 && o.end <= 23).sort((a, z) => z.end - a.end);
  console.log('AXE all ends:', r.axe.map(o => `${o.seed}:${o.end}/${o.final}`).join(' '));
  console.log('AXE good:', ax.slice(0, 6).map(o => JSON.stringify(o)).join('\n'));
  const gr = r.grow.filter(o => o.end >= 17 && o.end <= 25.5).sort((a, z) => z.lc - a.lc);
  console.log('GROW good:', gr.slice(0, 6).map(o => JSON.stringify(o)).join('\n'));
  await b.close(); })();
