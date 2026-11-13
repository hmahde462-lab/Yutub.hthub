// Picks seed/damage for each match so the fight ends naturally in 22-30 s and close. Winner = whatever the sim says.
const { chromium } = require('playwright'); const fs = require('fs');
const M = [
 ['العراق','السعودية','العراق ضد السعودية… منو ياخذها؟ 🔥'],
 ['مصر','المغرب','أقوى مواجهة عربية! 🔥'],
 ['البرازيل','الأرجنتين','كلاسيكو أمريكا الجنوبية ⚽'],
 ['العراق','الأردن','الأسود ضد النشامى 🦁'],
 ['الجزائر','تونس','ديربي المغرب العربي 🔥'],
 ['فرنسا','ألمانيا','عمالقة أوروبا وجهاً لوجه'],
 ['الكويت','قطر','معركة الخليج 🌊'],
 ['العراق','مصر','مين أقوى؟ العراق لو مصر؟'],
 ['إسبانيا','البرتغال','ديربي إيبيريا 🔥'],
 ['السعودية','الإمارات','الأخضر ضد الأبيض ⚔️'],
 ['المغرب','البرتغال','تتذكر 2022؟ الثأر هنا 🔥'],
 ['العراق','اليابان','العراق ضد اليابان… مفاجأة؟ 😱'],
 ['إنجلترا','إيطاليا','نهائي اليورو من جديد 🏆'],
 ['سوريا','لبنان','جيران بالحلبة 🔥'],
 ['أمريكا','المكسيك','حرب الجيران ⚔️'],
 ['العراق','البرازيل','العراق ضد البرازيل!! 😱'],
 ['الأرجنتين','فرنسا','نهائي كأس العالم من جديد 🏆'],
 ['السعودية','الأرجنتين','تتكرر مفاجأة 2022؟ 😱'],
 ['الجزائر','مصر','الفراعنة ضد محاربي الصحراء ⚔️'],
 ['العراق','الأرجنتين','الحلقة الأخيرة… العراق ضد ميسي وجماعته! 👑'],
];
const ARENAS = [{ R: 470, sides: 0 }, { R: 480, sides: 6, rot: 0 }, { R: 490, sides: 4, rot: Math.PI / 4 }, { R: 470, sides: 8, rot: Math.PI / 8 }];
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.addScriptTag({ path: __dirname + '/duel_engine.js' });
  const eps = [];
  for (const [i, [A, B, hook]] of M.entries()) { const arena = i === 19 ? { R: 480, sides: 0, shrinkFrom: 12, shrinkTo: 280, shrinkDur: 16 } : ARENAS[i % 4];
    const res = await p.evaluate(({ A, B, arena, base }) => { const out = [];
      for (const ds of [1.0, 1.3, 1.7, 2.2]) for (let s = 0; s < 40; s++) { const seed = base + s;
        const sim = new DuelSim(Object.assign({ seed, dmgScale: ds, cx: 540, cy: 1010, r: 66, maxTime: 60, spawnEvery: 1.5, fighters: [{ name: A }, { name: B }] }, arena));
        let minW = [100, 100]; while (sim.state === 'run') { sim.stepFrame(); sim.balls.forEach((x, k) => minW[k] = Math.min(minW[k], x.hp)); }
        out.push({ seed, ds, end: +sim.finaleT.toFixed(2), winner: sim.winner, minWin: minW[sim.winner], natural: sim.alive.length === 1 }); }
      return out; }, { A, B, arena, base: 1000 + i * 97 });
    const lo = 22, hi = i === 19 ? 34 : 30;
    const ok = res.filter(o => o.natural && o.end >= lo && o.end <= hi).sort((a, z) => a.minWin - z.minWin);
    const pick = ok[0] || res.filter(o => o.natural).sort((a, z) => Math.abs(a.end - 26) - Math.abs(z.end - 26))[0];
    eps.push({ n: i + 1, a: A, b: B, hook, seed: pick.seed, ds: pick.ds, dur: pick.end, winner: pick.winner, arena });
    console.log(i + 1, A, 'vs', B, '->', pick.winner ? B : A, JSON.stringify(pick)); }
  fs.writeFileSync('episodes.json', JSON.stringify(eps, null, 1)); await b.close(); })();
