// Seed search inside Chromium so results match the real render exactly.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.addScriptTag({ path: __dirname + '/battle_engine.js' });
  const res = await p.evaluate(() => { const out = [];
    for (let seed = 1; seed <= 250; seed++) { const s = new Battle({ seed }); const el = []; let leader = -1, ch = 0;
      while (s.state === 'run' && s.t < 27.5) { s.stepFrame(); if (s.frame % 6 === 0) { const n = s.counts(), m = Math.max(...n), tops = n.map((x, i) => x === m ? i : -1).filter(i => i >= 0);
          if (tops.length === 1 && tops[0] !== leader) { if (leader >= 0) ch++; leader = tops[0]; } }
        while (el.length < s.eliminated.length) el.push(+s.t.toFixed(1)); }
      const natural = s.counts().filter(x => x > 0).length === 1;
      out.push({ seed, end: +s.finaleT.toFixed(1), natural, ch, el, win: s.winner }); }
    return out; });
  const good = res.filter(o => o.natural && o.end >= 20 && o.end <= 26 && o.el[0] >= 7 && o.end - o.el[1] >= 4).sort((a, z) => z.ch - a.ch);
  console.log('natural', res.filter(o => o.natural).length, '/', res.length); console.log(good.slice(0, 8).map(o => JSON.stringify(o)).join('\n'));
  await b.close(); })();
