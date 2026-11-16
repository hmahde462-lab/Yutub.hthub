// HAMOUDI & MAMA, season (parts 8+): data-driven from SCORE.D. Pure function of t.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev, EP } = S; const D = S.D;
  const W = G.W, H = G.H;
  const CAST = {
    mama: { outfit: 'abaya', robe: '#1F1D26', hairStyle: 'hijab', hijab: '#2B2833', skin: '#D2A07A' },
    hamoudi: { outfit: 'tee', shirt: '#3C8DDB', bottoms: 'shorts', shorts: '#2E3A55', skin: '#D2A07A', hairStyle: 'short', hair: '#2A1D16', build: 'heavy' },
  };
  globalThis.CAST = CAST;
  const talk = (who, t) => { for (const l of S.vo) if (l.who === who && t >= l.at && t < l.at + l.dur - 0.05) { const a = t - l.at; return { open: 0.25 + 0.6 * Math.abs(Math.sin(a * 13)) * (0.6 + 0.4 * Math.sin(a * 3.1)), wide: 0.5 + 0.3 * Math.sin(a * 7), talking: true }; } return null; };
  const dark = (t) => D.dark && t >= ev.gag;

  // ---------- props ----------
  function controller(ctx, x, y, s) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); G.rrect(ctx, -70, -26, 140, 52, 24, { fill: '#2C2C34', lw: 4, seed: 70 }); G.ellipse(ctx, -40, 0, 11, 11, { fill: '#55556A', lw: 2, seed: 71 }); G.ellipse(ctx, 40, -8, 7, 7, { fill: '#E0503E', lw: 2, seed: 72 }); G.ellipse(ctx, 54, 6, 7, 7, { fill: '#3FA89B', lw: 2, seed: 73 }); ctx.restore(); }
  function router(ctx, x, y, s, t) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); G.rrect(ctx, -80, -30, 160, 60, 12, { fill: '#EDEDED', lw: 4, seed: 74 }); for (const ax of [-50, 50]) G.line(ctx, [[ax, -30], [ax * 1.2, -110]], { color: '#2A2A2A', lw: 6, seed: 75 + ax }); for (let k = 0; k < 4; k++) G.ellipse(ctx, -45 + k * 30, 0, 6, 6, { fill: Math.floor(t * 5 + k) % 2 ? '#3FD07A' : '#1E6B3D', lw: 0, seed: 77 + k }); ctx.restore(); }
  function paper(ctx, x, y, s, rot) { ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); G.rrect(ctx, -90, -120, 180, 240, 6, { fill: '#FBF6E8', lw: 4, seed: 80 }); for (let k = 0; k < 5; k++) G.line(ctx, [[-60, -70 + k * 30], [40, -70 + k * 30]], { color: '#9AA4B4', lw: 3, seed: 81 + k }); G.text(ctx, '٤', 50, 90, { size: 70, align: 'center', color: '#D62E2E', lang: 'ar', weight: 700 }); ctx.restore(); }
  function money(ctx, x, y, s, n = 4, rot = 0) { ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); for (let k = 0; k < n; k++) { ctx.save(); ctx.rotate((k - (n - 1) / 2) * 0.22); G.rrect(ctx, -30, -110, 60, 120, 6, { fill: '#6FBF73', lw: 3, seed: 90 + k }); G.ellipse(ctx, 0, -50, 16, 16, { fill: '#A6DBA0', lw: 2, seed: 95 + k }); ctx.restore(); } ctx.restore(); }
  function headset(ctx, x, y, s) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.strokeStyle = '#E0503E'; ctx.lineWidth = 12; ctx.beginPath(); ctx.arc(0, -95, 95, Math.PI * 1.05, Math.PI * 1.95); ctx.stroke(); G.rrect(ctx, -86, -10, 26, 44, 10, { fill: '#E0503E', lw: 3, seed: 100 }); G.rrect(ctx, 60, -10, 26, 44, 10, { fill: '#E0503E', lw: 3, seed: 101 }); G.line(ctx, [[-74, 30], [-40, 70], [-10, 72]], { color: '#2A2A2A', lw: 5, seed: 102 }); ctx.restore(); }
  function fan(ctx, x, y, s, t) { ctx.save(); ctx.translate(x, y); ctx.rotate(Math.sin(t * 9) * 0.35); ctx.scale(s, s); G.line(ctx, [[0, 0], [0, 120]], { color: '#8E6444', lw: 8, seed: 110 }); const p = []; for (let k = 0; k <= 8; k++) { const a = Math.PI * (1.15 + k * 0.0875); p.push([Math.cos(a) * 110, Math.sin(a) * 110]); } p.push([0, 0]); G.poly(ctx, p, { fill: '#E9C46A', lw: 4, seed: 111, step: 20, hatch: { color: 'rgba(140,90,30,0.35)', gap: 10 } }); ctx.restore(); }
  function candle(ctx, x, y, s, t) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); G.rrect(ctx, -16, -80, 32, 80, 4, { fill: '#F6F0E2', lw: 3, seed: 120 }); const f = 1 + 0.15 * Math.sin(t * 20); G.ellipse(ctx, 0, -100, 12 * f, 24 * f, { fill: '#F2B84B', lw: 2, seed: 121 }); ctx.restore(); }
  function star(ctx, x, y, r, fill) { const p = []; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.45 : r; p.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } G.poly(ctx, p, { fill, lw: 3, seed: 40 + Math.round(x), step: 12 }); }

  // ---------- the TV game (generic, made up) ----------
  function game(ctx, x, y, w, h, t) {
    ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    const mode = dark(t) ? 'off' : (D.tv === 'lost' && t < ev.gag ? 'race' : D.tv);
    ctx.fillStyle = '#1C2340'; ctx.fillRect(x, y, w, h);
    if (mode === 'off') { ctx.fillStyle = '#060608'; ctx.fillRect(x, y, w, h); }
    if (mode === 'race') {
      const sp = t * 900;
      ctx.fillStyle = '#3A3A48'; ctx.beginPath(); ctx.moveTo(x + w * 0.42, y + h * 0.28); ctx.lineTo(x + w * 0.58, y + h * 0.28); ctx.lineTo(x + w + 60, y + h); ctx.lineTo(x - 60, y + h); ctx.fill();
      for (let k = 0; k < 7; k++) { const u = ((k / 7) + sp / 2500) % 1, yy = y + h * 0.28 + h * 0.72 * u * u; ctx.fillStyle = '#F2D08A'; ctx.fillRect(x + w / 2 - 4 - 10 * u, yy, 8 + 20 * u, 10 + 50 * u * u); }
      const cx = x + w / 2 + Math.sin(t * 3.2) * w * 0.18, cy = y + h * 0.78;
      G.rrect(ctx, cx - 80, cy - 40, 160, 80, 18, { fill: '#3FA89B', lw: 4, seed: 90 }); G.rrect(ctx, cx - 55, cy - 70, 110, 40, 12, { fill: '#7FC4E8', lw: 4, seed: 91 });
      G.text(ctx, 'LAP 3/3', x + 30, y + 65, { size: 40, fam: 'Bungee', weight: 400, color: '#F2C23B' });
    }
    if (mode === 'lost') { ctx.fillStyle = '#2A0E14'; ctx.fillRect(x, y, w, h); G.text(ctx, 'NO CONNECTION', x + w / 2, y + h / 2 + 20, { size: 72, align: 'center', fam: 'Bungee', weight: 400, color: '#E0503E' }); }
    if (mode === 'football') {
      ctx.fillStyle = '#2F8A3E'; ctx.fillRect(x, y, w, h);
      for (let k = 0; k < 6; k++) { ctx.fillStyle = k % 2 ? '#2A7F38' : '#33944A'; ctx.fillRect(x + k * w / 6, y, w / 6, h); }
      ctx.strokeStyle = '#EAF6EA'; ctx.lineWidth = 5; ctx.strokeRect(x + 30, y + 30, w - 60, h - 60); ctx.beginPath(); ctx.moveTo(x + w / 2, y + 30); ctx.lineTo(x + w / 2, y + h - 30); ctx.stroke();
      ctx.strokeRect(x + w - 130, y + h / 2 - 90, 100, 180);
      const u = clamp(t / ev.gag); const bx = lerp(x + w * 0.3, x + w - 150, u), by = y + h / 2 + Math.sin(t * 6) * 40;
      G.ellipse(ctx, bx, by, 18, 18, { fill: '#FFFFFF', lw: 3, seed: 130 });
      G.text(ctx, '89:59', x + 30, y + 75, { size: 40, fam: 'Bungee', weight: 400, color: '#FFFFFF' });
    }
    if (mode === 'battle') {
      ctx.fillStyle = '#6E8F4E'; ctx.fillRect(x, y, w, h);
      for (let k = 0; k < 9; k++) G.ellipse(ctx, x + (k * 173) % w, y + (k * 97) % h, 50, 30, { fill: '#5A7A3E', lw: 0, seed: 140 + k });
      const r = lerp(260, 90, clamp(t / ev.gag)); ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 6; ctx.setLineDash([18, 12]); ctx.beginPath(); ctx.arc(x + w * 0.55, y + h * 0.5, r, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
      G.text(ctx, 'ALIVE: 2', x + 30, y + 65, { size: 40, fam: 'Bungee', weight: 400, color: '#FFFFFF' });
      if (t >= ev.gag) { ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.fillRect(x, y, w, h); G.text(ctx, 'WINNER! 🍗', x + w / 2, y + h / 2 + 30, { size: 90, align: 'center', fam: 'Bungee', weight: 400, color: '#F2C23B' }); }
    }
    if (mode === 'shop') { ctx.fillStyle = '#2B1E4A'; ctx.fillRect(x, y, w, h); G.text(ctx, 'STORE', x + w / 2, y + 110, { size: 70, align: 'center', fam: 'Bungee', weight: 400, color: '#F2C23B' }); for (let k = 0; k < 3; k++) { G.rrect(ctx, x + 80 + k * 280, y + 170, 220, 320, 20, { fill: '#433070', lw: 4, seed: 150 + k }); G.ellipse(ctx, x + 190 + k * 280, y + 300, 60, 60, { fill: '#F2C23B', lw: 4, seed: 155 + k }); G.text(ctx, '$' + (5 + k * 10), x + 190 + k * 280, y + 450, { size: 44, align: 'center', fam: 'Bungee', weight: 400, color: '#FFFFFF' }); } }
    ctx.restore();
  }
  function tv(ctx, t) { const x = 70, y = 230, w = 940, h = 600; G.rrect(ctx, x - 24, y - 24, w + 48, h + 48, 22, { fill: '#17171C', lw: 6, seed: 60 }); game(ctx, x, y, w, h, t); }
  function room(ctx, t) {
    ctx.fillStyle = '#3B3350'; ctx.fillRect(0, 0, W, H);
    G.rrect(ctx, -20, 0, W + 40, 1260, 0, { fill: D.day ? '#7A6A94' : '#5A4E78', lw: 0, seed: 1, hatch: { color: 'rgba(0,0,0,0.12)', gap: 16 } });
    if (D.day) { G.rrect(ctx, 760, 900, 220, 260, 8, { fill: '#9FD4F0', lw: 5, seed: 2 }); G.ellipse(ctx, 900, 960, 30, 30, { fill: '#F6D24A', lw: 2, seed: 3 }); } // daytime
    else { G.rrect(ctx, 760, 900, 220, 260, 8, { fill: '#1A2244', lw: 5, seed: 2 }); G.ellipse(ctx, 900, 960, 30, 30, { fill: '#F6EFC8', lw: 2, seed: 3 }); }
    G.rrect(ctx, -20, 1260, W + 40, 700, 0, { fill: '#6E4E3A', lw: 4, seed: 4, hatch: { color: 'rgba(0,0,0,0.15)', gap: 14 } });
    G.ellipse(ctx, 540, 1700, 470, 120, { fill: '#9C2F3A', lw: 4, seed: 5, hatch: { color: 'rgba(242,184,75,0.4)', gap: 18 } });
  }
  function sofa(ctx, x, y) { G.rrect(ctx, x - 300, y - 230, 600, 170, 30, { fill: '#7A8C5A', lw: 5, seed: 20 }); G.rrect(ctx, x - 340, y - 110, 680, 120, 26, { fill: '#8FA36A', lw: 5, seed: 21 }); G.rrect(ctx, x - 360, y - 170, 70, 180, 24, { fill: '#7A8C5A', lw: 5, seed: 22 }); G.rrect(ctx, x + 290, y - 170, 70, 180, 24, { fill: '#7A8C5A', lw: 5, seed: 23 }); }
  function blackout(ctx, t, glow, a = 0.82) { // darkness with a candle or moonlight glow
    ctx.save(); ctx.fillStyle = `rgba(6,6,14,${a})`; ctx.fillRect(0, 0, W, H);
    if (glow) { const g = ctx.createRadialGradient(glow[0], glow[1], 10, glow[0], glow[1], 520); g.addColorStop(0, 'rgba(255,190,90,0.45)'); g.addColorStop(1, 'rgba(255,190,90,0)'); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); }
    ctx.restore();
  }

  function emo(ctx, e, x, y, size, rot = 0) { if (!e) return; ctx.save(); ctx.translate(x, y); ctx.rotate(rot); G.text(ctx, e, 0, size * 0.35, { size, align: 'center' }); ctx.restore(); }
  const FACE = { sad: ['normal', 'worried', 'wavy'], scared: ['wide', 'worried', 'o'], grin: ['happy', 'up', 'grin'], worried: ['wide', 'worried', 'wavy'] };

  // ---------- shots ----------
  function mamaWalk(ctx, t, y, s, u, mm, prop) {
    const mx = lerp(1250, 860, ease.outQuad(u));
    Ch.person(ctx, { x: mx, y, s, sx: -1, ...(u < 1 ? { pose: 'walk', walk: t * 3.2 } : { pose: 'stand' }), style: CAST.mama, handR: u >= 1 ? [80, -320] : null, eyes: 'normal', brows: 'determined', mouth: mm || 'smirk', look: -0.6, seed: 400 });
    if (prop) emo(ctx, prop, u >= 1 ? mx - s * 80 : mx - s * 60, u >= 1 ? y - s * 320 - 40 : y - s * 200, 120 * s, Math.sin(t * 5) * 0.08);
  }
  function wide(ctx, t) {
    room(ctx, t); tv(ctx, t); sofa(ctx, 540, 1330);
    G.ellipse(ctx, 540, 1690, 170, 40, { fill: '#E0A13E', lw: 4, seed: 30 });
    const hm = talk('hamoudi', t), mm = talk('mama', t);
    const u = clamp((t - 0.9) / 1.4);
    if (D.w === 'sofa') {
      Ch.person(ctx, { x: 540, y: 1250, s: 0.8, pose: 'sit', style: CAST.hamoudi, handL: [-60, -120], handR: [70, -170], eyes: dark(t) ? 'wide' : 'happy', brows: 'up', mouth: hm || 'grin', seed: 300 });
      emo(ctx, D.hp, 540 + 0.8 * 70, 1250 - 0.8 * 170 - 20, 110, Math.sin(t * 4) * 0.1);
      mamaWalk(ctx, t, 1760, 0.95, u, mm, D.mp);
    } else {
      Ch.person(ctx, { x: 540, y: 1680, s: 1.0, pose: 'sit', rot: Math.sin(t * 3) * 0.06, style: CAST.hamoudi, handL: [-45, -95], handR: [45, -95], eyes: 'wide', brows: dark(t) ? 'worried' : 'determined', mouth: hm || (dark(t) ? 'o' : 'flat'), lookY: -0.6, seed: 300 });
      controller(ctx, 540, 1680 - 95, 0.72);
      mamaWalk(ctx, t, 1520, 0.8, u, mm, D.mp);
    }
    if (!dark(t)) { ctx.save(); ctx.globalAlpha = 0.08 + 0.04 * Math.sin(t * 9); ctx.fillStyle = '#7FB8FF'; ctx.fillRect(0, 860, W, H); ctx.restore(); }
    if (dark(t)) blackout(ctx, t, null);
  }
  function gag(ctx, t) {
    const a = t - ev.gag, pop = ease.outBack(clamp(a / 0.2), 2.6);
    ctx.fillStyle = D.bg; ctx.fillRect(0, 0, W, H);
    G.rays(ctx, 540, 900, { n: 28, r0: 150, r1: 1800, color: 'rgba(255,255,255,0.22)', lw: 14, seed: 7, spin: a * 0.5 });
    const light = ['#F6F0E2', '#F2C23B', '#7FC4E8', '#E9A23B', '#E07A9E'].includes(D.bg);
    ctx.save(); ctx.translate(540, 860); ctx.scale(pop, pop);
    emo(ctx, D.ge, 0, -150, 380, Math.sin(a * 9) * 0.08);
    G.text(ctx, D.gt, 0, 300, { size: D.gt.length > 14 ? 92 : 118, align: 'center', color: light ? '#14121C' : '#FFFFFF', stroke: light ? '#FFFFFF' : '#14121C', strokeW: 12, lang: 'ar' });
    ctx.restore();
  }
  function close(ctx, t, who) {
    room(ctx, t);
    const m = talk(who, t);
    if (who === 'hamoudi') {
      sofa(ctx, 540, 1900);
      const after = t >= ev.gag, f = after ? FACE[D.face] : ['wide', 'up', 'o'];
      Ch.person(ctx, { x: 540, y: 1780, s: 1.9, pose: 'sit', style: CAST.hamoudi, eyes: f[0], brows: f[1], mouth: m || f[2], gesture: after && D.face !== 'grin' ? 'shrug' : 'point', sweat: after && D.face !== 'grin' ? 0.9 : 0, seed: 300 });
      if (after && D.face === 'sad') for (const sx of [-1, 1]) { const k = (t * 1.5) % 1; G.ellipse(ctx, 540 + sx * 70, 1780 - 1.9 * 360 + k * 120, 10, 16, { fill: '#7FC4E8', lw: 2, seed: 160 + sx }); }
    } else {
      const s = 2.0;
      Ch.person(ctx, { x: 540, y: 2120, s, pose: 'stand', style: CAST.mama, brows: 'determined', eyes: 'normal', mouth: m || 'smirk', handR: [130, -330], handL: [-90, -250], gesture: null, seed: 400 });
      emo(ctx, D.mp, 540 + s * 130, 2120 - s * 330 - 60, 200, Math.sin(t * 4) * 0.08);
      if (m) for (let k = 0; k < 3; k++) G.line(ctx, [[250 + k * 30, 560 - k * 40], [210 + k * 30, 520 - k * 40]], { color: '#E0503E', lw: 9, seed: 95 + k });
    }
    if (dark(t)) blackout(ctx, t, null, 0.6);
  }
  function endCard(ctx, t) {
    const e = clamp((t - ev.end) / 0.5); if (e <= 0) return;
    ctx.save(); ctx.globalAlpha = e; ctx.fillStyle = 'rgba(16,12,28,0.8)'; ctx.fillRect(0, 0, W, H);
    const pop = ease.outBack(e, 2); ctx.translate(540, 820); ctx.scale(pop, pop);
    G.text(ctx, 'حمودي وماما', 0, -80, { size: 140, align: 'center', color: '#F2C23B', stroke: '#1A1A22', strokeW: 14, lang: 'ar' });
    G.text(ctx, 'الجزء ' + EP + ': ' + S.TITLE, 0, 90, { size: S.TITLE.length > 10 ? 76 : 90, align: 'center', color: '#FFFFFF', lang: 'ar' });
    G.text(ctx, S.LAST ? 'نهاية الموسم الأول ❤️' : 'تابعنا للجزء ' + (EP + 1) + ' 👇', 0, 250, { size: 70, align: 'center', color: '#E8E4FF', lang: 'ar' });
    ctx.restore();
  }
  function caption(ctx, t) {
    for (const l of S.vo) if (t >= l.at && t < l.at + l.dur + 0.2) {
      const k = ease.outBack(clamp((t - l.at) / 0.2), 2);
      ctx.save(); ctx.translate(540, 935); ctx.scale(k, k);
      G.rrect(ctx, -510, -62, 1020, 96, 26, { fill: 'rgba(14,12,22,0.85)', lw: 0, seed: 99 });
      const size = l.text.length > 38 ? 38 : l.text.length > 32 ? 44 : 50;
      G.text(ctx, l.text, 0, 0, { size, align: 'center', color: l.who === 'mama' ? '#FFD86B' : '#9FD4FF', lang: 'ar' });
      ctx.restore();
    }
  }
  function badge(ctx, t) { const a = clamp(1 - (t - 2) / 0.4); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; G.rrect(ctx, 300, 240, 480, 90, 45, { fill: '#E0503E', lw: 4, seed: 98 }); G.text(ctx, 'الجزء ' + EP + ' 🎮', 540, 302, { size: 54, align: 'center', color: '#FFFFFF', lang: 'ar' }); ctx.restore(); }

  Studio.film({
    post: { vignette: 0.3, grain: 0.04, paper: 0.3 },
    fadeOut: 0.6,
    draw(ctx, t) {
      let i = 0; while (i + 1 < S.shots.length && t >= S.shots[i + 1].t0) i++;
      const sh = S.shots[i], local = t - sh.t0;
      const z = 1 + 0.04 * clamp(local / 4);
      const shake = sh.kind === 'gag' ? 22 * Math.exp(-local * 5) : 0;
      ctx.save(); ctx.translate(W / 2 + U.noise1(t * 30, 1) * shake, H / 2 + U.noise1(t * 30, 2) * shake); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
      if (sh.kind === 'close') close(ctx, t, sh.who); else if (sh.kind === 'gag') gag(ctx, t); else wide(ctx, t);
      ctx.restore();
      const f = 1 - clamp(local / 0.12); if (i > 0 && f > 0) { ctx.fillStyle = `rgba(255,255,255,${0.7 * f})`; ctx.fillRect(0, 0, W, H); }
      if (t < ev.end) caption(ctx, t);
      badge(ctx, t);
      endCard(ctx, t);
    },
  });
})();
