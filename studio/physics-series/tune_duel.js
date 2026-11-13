const { chromium } = require('playwright'); const fs = require('fs'); const SPECS = require('./series_duel.js');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/duel_engine.js' });
  const res = {};
  for (const [n, sp] of SPECS.entries()) {
    let fighters;
    if (sp.rematch) { const r = res[sp.rematch], W = r.fighters[r.winner], L = r.fighters[r.firstKo ?? (r.winner ? 0 : 1)]; fighters = [L, W]; }
    else if (sp.champions) fighters = sp.champions.map(id => { const r = res[id]; return r.fighters[r.winner]; });
    else fighters = sp.fighters.map(([name, color]) => ({ name, color }));
    const r = await p.evaluate(({ base, fighters }) => { const out = [];
      for (const ds of [1.4, 1.8, 2.2, 2.7]) for (let seed = 1; seed <= 30; seed++) { const s = new DuelSim(Object.assign({ seed, dmgScale: ds, fighters, maxTime: 40, spawnEvery: 1.7 }, base)); let minW = {}; 
        while (s.state === 'run') { s.stepFrame(); for (const bb of s.balls) minW[bb.i] = Math.min(minW[bb.i] ?? 100, bb.hp); }
        const kos = s.events.filter(e => e.kind === 'ko'); out.push({ seed, ds, end: +s.finaleT.toFixed(1), winner: s.winner, minWinHp: minW[s.winner], kos: kos.length, firstKo: kos.length ? kos[0].who : null, natural: s.alive.length === 1 }); }
      return out; }, { base: sp.sim, fighters });
    const good = r.filter(o => o.natural && o.end >= 21 && o.end <= 32).sort((a, z) => a.minWinHp - z.minWinHp);
    const pick = good[0] || r.filter(o => o.natural).sort((a, z) => Math.abs(a.end - 27) - Math.abs(z.end - 27))[0] || r[0];
    res[sp.id] = Object.assign({ fighters }, pick);
    const ep = { id: sp.id, template: 'duel.html', title: sp.title, partLabel: 'قتال ' + (n + 1), hook: sp.hook, endSub: sp.endSub, bg: sp.bg, floor: sp.floor, ring: sp.ring, fighters,
      sim: Object.assign({ seed: pick.seed, dmgScale: pick.ds, maxTime: 40, spawnEvery: 1.7 }, sp.sim) };
    if (sp.rematch) ep.hook = `${fighters[0].name} رجع ينتقم من ${fighters[1].name}!`;
    fs.writeFileSync(`episodes/${sp.id}.json`, JSON.stringify(ep, null, 1));
    console.log(sp.id, fighters.map(f => f.name).join(','), JSON.stringify(pick), 'good', good.length); }
  await b.close(); })();
