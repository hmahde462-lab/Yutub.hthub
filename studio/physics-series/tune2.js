const { chromium } = require('playwright'); const fs = require('fs'); const SPECS = require('./series2.js');
const only = process.argv[2];
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/arena_engine.js' });
  for (const sp of SPECS) { if (only && sp.id !== only) continue;
    const res = await p.evaluate((base) => { const out = [];
      for (const m of [0.6, 0.8, 1, 1.25, 1.6]) for (const g of [700, 900, 1100]) {
        const cfg = JSON.parse(JSON.stringify(base)); cfg.g = g; cfg.maxTime = 30; cfg.cutters.forEach(k => { if (k.spin) k.spin *= m; if (k.speed) k.speed *= m; }); if (cfg.container.spin) cfg.container.spin *= Math.sqrt(m);
        const s = new ArenaSim(cfg); while (s.state === 'run' && s.t < 30) s.stepFrame();
        out.push({ m, g, end: +(s.finaleT || 0).toFixed(1), final: s.finalCount, cfg }); }
      return out; }, sp.sim);
    const maxF = Math.max(...res.map(r => r.final));
    const ok = res.filter(r => r.end >= 16 && r.end <= 25 && r.final >= maxF * .9).sort((a, z) => Math.abs(a.end - 21) - Math.abs(z.end - 21));
    let pick = ok[0]; let capped = false;
    if (!pick) { capped = true; const r2 = await p.evaluate((base) => { const out = []; for (const m of [0.8, 1, 1.25, 1.6, 2]) for (const g of [700, 900, 1100]) { const cfg = JSON.parse(JSON.stringify(base)); cfg.g = g; cfg.maxTime = 24.5; cfg.cutters.forEach(k => { if (k.spin) k.spin *= m; if (k.speed) k.speed *= m; }); if (cfg.container.spin) cfg.container.spin *= Math.sqrt(m);
        const s = new ArenaSim(cfg); while (s.state === 'run' && s.t < 25) s.stepFrame(); out.push({ m, g, end: +(s.finaleT || 0).toFixed(1), final: s.finalCount, cfg }); } return out; }, sp.sim);
      pick = r2.sort((a, z) => z.final - a.final)[0]; }
    const ep = Object.assign({}, sp, { template: 'arena.html', counterLabel: 'كرة', sim: pick.cfg }); ep.sim.maxTime = capped ? 24.5 : 30; const ms = [50, 100, 150, 200, 250].filter(v => v <= pick.final - 8).pop(); ep.milestone = ms; ep.milestoneText = `تجاوزنا ${ms}! 🔥`;
    fs.writeFileSync(`episodes/${sp.id}.json`, JSON.stringify(ep, null, 1));
    console.log(sp.id, 'pick m', pick.m, 'g', pick.g, 'end', pick.end, 'final', pick.final, '| options', res.map(r => `${r.m}/${r.g}:${r.end}/${r.final}`).join(' ')); }
  await b.close(); })();
