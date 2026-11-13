const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/battle_engine.js' });
  const r = await p.evaluate(() => { const out = [];
    for (let seed = 1; seed <= 400; seed++) { const s = new Battle({ seed, ballR: 38, perTeam: 8, maxTime: 27 }); let lead = -1, lc = 0, minWin = 99;
      while (s.state === 'run') { s.stepFrame(); const n = s.counts(), m = Math.max(...n), l = n.indexOf(m); if (n.filter(x => x === m).length === 1 && l !== lead) { if (lead >= 0) lc++; lead = l; } }
      const w = s.winner; for (const h of s.history) minWin = Math.min(minWin, h[w]);
      const natural = s.counts ? s.finalCounts.filter(x => x > 0).length === 1 : false;
      out.push({ seed, end: +s.finaleT.toFixed(1), winner: w, lc, minWin, natural }); }
    return out; });
  const good = r.filter(o => o.natural && o.end >= 17 && o.end <= 25 && o.minWin <= 3).sort((a, z) => z.lc - a.lc);
  console.log(good.slice(0, 12).map(o => JSON.stringify(o)).join('\n'));
  await b.close(); })();
