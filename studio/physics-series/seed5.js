const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/ball2_engine.js' });
  const r = await p.evaluate(() => { const out = [];
    for (const spin of [1.2, 1.5, 1.8]) for (const g of [700, 900]) for (let seed = 1; seed <= 25; seed++) {
      const s = new AxeSim({ seed, spin, g, axes: 2, rMin: 8, maxTime: 30 }); let t100 = null;
      while (s.state === 'run' && s.t < 30) { s.stepFrame(); if (t100 === null && s.count >= 100) t100 = s.t; }
      out.push({ seed, spin, g, end: +(s.finaleT || 0).toFixed(1), final: s.finalCount, t100: t100 && +t100.toFixed(1) }); }
    return out; });
  const good = r.filter(o => o.final >= 100 && o.end >= 17 && o.end <= 24 && o.end - o.t100 >= 1.5).sort((a, z) => (z.t100 - a.t100));
  console.log(good.slice(0, 10).map(o => JSON.stringify(o)).join('\n')); console.log('total', r.length, 'good', good.length);
  await b.close(); })();
