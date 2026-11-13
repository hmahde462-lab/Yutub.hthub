const { chromium } = require('playwright'); const fs = require('fs'); const SPECS = require('./series_battle.js');
const ids = process.argv.slice(2);
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/battle_engine.js' });
  SPECS.forEach((sp, i) => sp.n = i + 1);
  for (const sp of SPECS) { if (ids.length && !ids.includes(sp.id)) continue;
    let ep;
    if (sp.from) { ep = JSON.parse(fs.readFileSync(`episodes/${sp.from}.json`)); }
    else { const base = Object.assign({ teams: sp.teams.length, maxTime: 27 }, sp.sim);
      const r = await p.evaluate((base) => { const out = [];
        for (let seed = 1; seed <= 300; seed++) { const s = new Battle(Object.assign({ seed }, base)); let lead = -1, lc = 0, minWin = 99;
          while (s.state === 'run') { s.stepFrame(); const n = s.counts(), m = Math.max(...n), l = n.indexOf(m); if (n.filter(x => x === m).length === 1 && l !== lead) { if (lead >= 0) lc++; lead = l; } }
          for (const h of s.history) minWin = Math.min(minWin, h[s.winner]);
          out.push({ seed, end: +s.finaleT.toFixed(1), winner: s.winner, lc, minWin, natural: s.finalCounts.filter(x => x > 0).length === 1 }); }
        return out; }, base);
      const good = r.filter(o => o.natural && o.end >= 16 && o.end <= 25).sort((a, z) => (a.minWin - z.minWin) * 3 + (z.lc - a.lc) * .2);
      const pick = good[0] || r.sort((a, z) => Math.abs(a.end - 21) - Math.abs(z.end - 21))[0];
      console.log(sp.id, JSON.stringify(pick), 'good', good.length);
      ep = { id: sp.id, template: 'battle.html', title: sp.title, hook: sp.hook, endSub: sp.endSub, noGlow: true, theme: sp.theme, ballStyle: sp.ballStyle, teams: sp.teams, sim: Object.assign({ seed: pick.seed }, base) }; }
    ep.id = sp.id; ep.partLabel = 'معركة ' + sp.n; ep.noGlow = true;
    fs.writeFileSync(`episodes/${sp.id}.json`, JSON.stringify(ep, null, 1)); }
  await b.close(); })();
