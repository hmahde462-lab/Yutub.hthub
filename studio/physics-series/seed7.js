const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/ball2_engine.js' });
  const r = await p.evaluate(() => { const out = [];
    for (const spin of [0.7, 0.9, 1.1]) for (const rMin of [5.5, 6]) for (const g of [700, 900]) {
      const s = new AxeSim({ spin, g, axes: 3, rMin, maxTime: 32 }); let t200 = null;
      while (s.state === 'run' && s.t < 32) { s.stepFrame(); if (t200 === null && s.count >= 200) t200 = s.t; }
      out.push({ spin, rMin, g, end: +(s.finaleT || 0).toFixed(1), final: s.finalCount, t200: t200 && +t200.toFixed(1) }); }
    return out; });
  console.log(r.map(o => JSON.stringify(o)).join('\n')); await b.close(); })();
