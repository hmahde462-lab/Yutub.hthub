const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/ball2_engine.js' });
  const r = await p.evaluate(() => { const axe = [], grow = [];
    for (const spin of [2.6, 3.0, 3.4]) for (const g of [900, 1200]) { const s = new AxeSim({ spin, g }); while (s.state === 'run' && s.t < 26) s.stepFrame(); axe.push(`spin${spin} g${g}: end ${s.finaleT.toFixed(1)} n ${s.finalCount}`); }
    for (const gr of [1.03, 1.04]) for (let seed = 1; seed <= 25; seed++) { const s = new GrowSim({ seed, grow: gr }); while (s.state === "run" && s.t < 30) s.stepFrame(); grow.push({ grow: gr, seed, end: +s.finaleT.toFixed(1), lc: s.leadChanges }); }
    return { axe, grow }; });
  console.log(r.axe.join('\n'));
  for (const gv of [1.03, 1.04]) console.log(gv, r.grow.filter(o => o.grow === gv).map(o => `${o.seed}:${o.end}/${o.lc}`).join(' '));
  await b.close(); })();
