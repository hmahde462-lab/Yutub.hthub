// Plays the whole 16-team knockout in Chromium (deterministic), picking per-match seed/damage so each match lasts the target time
// and ends close. Winners are whatever the simulation produces. Writes episodes/tour1.json.
const { chromium } = require('playwright'); const fs = require('fs');
const TEAMS = ['العراق','البرازيل','السعودية','الأرجنتين','مصر','إسبانيا','المغرب','البرتغال','الجزائر','فرنسا','ألمانيا','اليابان','إنجلترا','إيطاليا','هولندا','أمريكا'];
const ROUNDS = [
  { name: 'دور الـ16', target: [19, 25], arena: { R: 400, sides: 0 } },
  { name: 'ربع النهائي', target: [23, 29], arena: { R: 400, sides: 6, rot: 0 } },
  { name: 'نصف النهائي', target: [27, 33], arena: { R: 400, sides: 4, rot: Math.PI / 4 } },
  { name: 'النهائي', target: [35, 45], arena: { R: 420, sides: 0, shrinkFrom: 14, shrinkTo: 250, shrinkDur: 20 } },
];
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/duel_engine.js' });
  let alive = TEAMS.slice(); const matches = []; let seedBase = 1;
  for (const [ri, rd] of ROUNDS.entries()) { const next = [];
    for (let m = 0; m < alive.length; m += 2) { const A = alive[m], B = alive[m + 1];
      const res = await p.evaluate(({ A, B, rd, seedBase }) => { const out = [];
        for (const ds of [1.0, 1.3, 1.7, 2.2]) for (let s = 0; s < 40; s++) { const seed = seedBase + s;
          const sim = new DuelSim(Object.assign({ seed, dmgScale: ds, cx: 560, cy: 590, r: 58, maxTime: 60, spawnEvery: 1.6, fighters: [{ name: A }, { name: B }] }, rd.arena));
          let minW = [100, 100]; while (sim.state === 'run') { sim.stepFrame(); sim.balls.forEach((x, i) => minW[i] = Math.min(minW[i], x.hp)); }
          out.push({ seed, ds, end: +sim.finaleT.toFixed(2), winner: sim.winner, minWin: minW[sim.winner], natural: sim.alive.length === 1, lead: 0 }); }
        return out; }, { A, B, rd, seedBase });
      const ok = res.filter(o => o.natural && o.end >= rd.target[0] && o.end <= rd.target[1]).sort((a, z) => a.minWin - z.minWin);
      const pick = ok[0] || res.filter(o => o.natural).sort((a, z) => Math.abs(a.end - (rd.target[0] + rd.target[1]) / 2) - Math.abs(z.end - (rd.target[0] + rd.target[1]) / 2))[0];
      const W = pick.winner === 0 ? A : B; next.push(W); seedBase += 50;
      matches.push({ round: ri, roundName: rd.name, a: A, b: B, seed: pick.seed, ds: pick.ds, dur: pick.end, winner: pick.winner, arena: rd.arena });
      console.log(rd.name, A, 'vs', B, '->', W, JSON.stringify(pick)); }
    alive = next; }
  fs.writeFileSync('episodes/tour1.json', JSON.stringify({ id: 'tour1', teams: TEAMS, rounds: ROUNDS.map(r => r.name), matches, champion: alive[0] }, null, 1));
  console.log('CHAMPION', alive[0], 'total match time', matches.reduce((s, m) => s + m.dur, 0).toFixed(1)); await b.close(); })();
