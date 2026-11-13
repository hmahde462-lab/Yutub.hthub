// Season 2: 61 matches alternating country/club, episodes 21..81. Same tuning rule as tune.js.
const { chromium } = require('playwright'); const fs = require('fs');
const MM = JSON.parse(fs.readFileSync(__dirname + '/matches2.json', 'utf8')); const M = [];
for (let i = 0; i < 31; i++) { M.push(MM.country[i]); if (MM.club[i]) M.push(MM.club[i]); }
const ARENAS = [{ R: 470, sides: 0 }, { R: 480, sides: 6, rot: 0 }, { R: 490, sides: 4, rot: Math.PI / 4 }, { R: 470, sides: 8, rot: Math.PI / 8 }, { R: 480, sides: 0, shrinkFrom: 12, shrinkTo: 300, shrinkDur: 16 }];
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/duel_engine.js' });
  const eps = [];
  for (const [i, [A, B, hook]] of M.entries()) { const arena = ARENAS[i % 5], n = 21 + i;
    const res = await p.evaluate(({ A, B, arena, base }) => { const out = [];
      for (const ds of [1.0, 1.3, 1.7, 2.2]) for (let s = 0; s < 40; s++) { const seed = base + s;
        const sim = new DuelSim(Object.assign({ seed, dmgScale: ds, cx: 540, cy: 1010, r: 66, maxTime: 60, spawnEvery: 1.5, fighters: [{ name: A }, { name: B }] }, arena));
        let minW = [100, 100]; while (sim.state === 'run') { sim.stepFrame(); sim.balls.forEach((x, k) => minW[k] = Math.min(minW[k], x.hp)); }
        out.push({ seed, ds, end: +sim.finaleT.toFixed(2), winner: sim.winner, minWin: minW[sim.winner], natural: sim.alive.length === 1 }); }
      return out; }, { A, B, arena, base: 5000 + n * 97 });
    const hi = arena.shrinkFrom ? 34 : 30;
    const ok = res.filter(o => o.natural && o.end >= 22 && o.end <= hi).sort((a, z) => a.minWin - z.minWin);
    const pick = ok[0] || res.filter(o => o.natural).sort((a, z) => Math.abs(a.end - 26) - Math.abs(z.end - 26))[0];
    eps.push({ n, a: A, b: B, hook, seed: pick.seed, ds: pick.ds, dur: pick.end, winner: pick.winner, arena });
    console.log(n, A, 'vs', B, '->', pick.winner ? B : A, pick.end); }
  fs.writeFileSync(__dirname + '/episodes2.json', JSON.stringify(eps, null, 1)); await b.close(); })();
