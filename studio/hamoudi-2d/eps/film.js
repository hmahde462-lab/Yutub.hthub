// HAMOUDI & MAMA, parts 3-7: one film file, the episode comes from SCORE.EP. Pure function of t.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev, EP } = S;
  const W = G.W, H = G.H;
  const CAST = {
    mama: { outfit: 'abaya', robe: '#1F1D26', hairStyle: 'hijab', hijab: '#2B2833', skin: '#D2A07A' },
    hamoudi: { outfit: 'tee', shirt: '#3C8DDB', bottoms: 'shorts', shorts: '#2E3A55', skin: '#D2A07A', hairStyle: 'short', hair: '#2A1D16', build: 'heavy' },
  };
  globalThis.CAST = CAST;
  const talk = (who, t) => { for (const l of S.vo) if (l.who === who && t >= l.at && t < l.at + l.dur - 0.05) { const a = t - l.at; return { open: 0.25 + 0.6 * Math.abs(Math.sin(a * 13)) * (0.6 + 0.4 * Math.sin(a * 3.1)), wide: 0.5 + 0.3 * Math.sin(a * 7), talking: true }; } return null; };
  const dark = (t) => EP === 6 && t >= ev.gag; // the power cut

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
    const mode = EP === 6 ? (dark(t) ? 'off' : 'football') : EP === 5 ? 'battle' : EP === 7 ? 'shop' : EP === 3 && t >= ev.gag ? 'lost' : 'race';
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
    G.rrect(ctx, -20, 0, W + 40, 1260, 0, { fill: EP === 7 || EP === 4 ? '#7A6A94' : '#5A4E78', lw: 0, seed: 1, hatch: { color: 'rgba(0,0,0,0.12)', gap: 16 } });
    if (EP === 7 || EP === 4) { G.rrect(ctx, 760, 900, 220, 260, 8, { fill: '#9FD4F0', lw: 5, seed: 2 }); G.ellipse(ctx, 900, 960, 30, 30, { fill: '#F6D24A', lw: 2, seed: 3 }); } // daytime
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

  // ---------- shots ----------
  function wide(ctx, t) {
    room(ctx, t); tv(ctx, t); sofa(ctx, 540, 1330);
    G.ellipse(ctx, 540, 1690, 170, 40, { fill: '#E0A13E', lw: 4, seed: 30 });
    const hm = talk('hamoudi', t), mm = talk('mama', t);
    if (EP === 5) { // mama plays, Hamoudi begs from the sofa
      Ch.person(ctx, { x: 470, y: 1250, s: 0.7, pose: 'sit', style: CAST.hamoudi, gesture: 'dua', eyes: 'normal', brows: 'worried', mouth: hm || 'wavy', seed: 300 });
      Ch.person(ctx, { x: 540, y: 1680, s: 1.05, pose: 'sit', rot: Math.sin(t * 3) * 0.06, style: CAST.mama, handL: [-45, -95], handR: [45, -95], eyes: 'wide', brows: 'determined', mouth: mm || 'flat', lookY: -0.6, seed: 400 });
      headset(ctx, 540, 1680 - 1.05 * 300, 1.05); controller(ctx, 540, 1680 - 1.05 * 95, 0.75);
    } else if (EP === 7) { // Hamoudi on the sofa with his Eid money
      Ch.person(ctx, { x: 540, y: 1250, s: 0.8, pose: 'sit', style: CAST.hamoudi, handL: [-60, -120], handR: [70, -170], eyes: 'happy', brows: 'up', mouth: hm || 'grin', seed: 300 });
      money(ctx, 540 + 0.8 * 70, 1250 - 0.8 * 170, 0.7, 5, Math.sin(t * 4) * 0.1);
      const u = clamp((t - 1.2) / 1.6); // mama comes in
      Ch.person(ctx, { x: lerp(1250, 850, ease.outQuad(u)), y: 1760, s: 0.95, sx: -1, ...(u < 1 ? { pose: 'walk', walk: t * 3.2 } : { pose: 'stand' }), style: CAST.mama, eyes: 'happy', brows: 'up', mouth: mm || 'smirk', look: -0.6, seed: 400 });
    } else { // Hamoudi plays on the cushion
      Ch.person(ctx, { x: 540, y: 1680, s: 1.0, pose: 'sit', rot: Math.sin(t * 3) * 0.06, style: CAST.hamoudi, handL: [-45, -95], handR: [45, -95], eyes: dark(t) ? 'wide' : 'wide', brows: dark(t) ? 'worried' : 'determined', mouth: hm || (dark(t) ? 'o' : 'flat'), lookY: -0.6, seed: 300 });
      controller(ctx, 540, 1680 - 95, 0.72);
      if (EP === 3) { G.rrect(ctx, 860, 1130, 200, 30, 4, { fill: '#8E6444', lw: 4, seed: 33 }); const u = clamp((t - 1.0) / 1.4); const mx = lerp(1250, 930, ease.outQuad(u)); Ch.person(ctx, { x: mx, y: 1500, s: 0.8, sx: -1, ...(u < 1 ? { pose: 'walk', walk: t * 3.2 } : { pose: 'stand' }), style: CAST.mama, handR: u >= 1 ? [70, -300] : null, eyes: 'normal', brows: 'determined', mouth: 'smirk', seed: 400 }); router(ctx, u >= 1 ? mx - 0.8 * 70 : 960, u >= 1 ? 1500 - 0.8 * 300 : 1100, 0.7, t); }
      if (EP === 4) { const u = clamp((t - 0.2) / 0.9); const mx = lerp(1250, 880, ease.outQuad(u)); Ch.person(ctx, { x: mx, y: 1560, s: 0.85, sx: -1, ...(u < 1 ? { pose: 'walk', walk: t * 3.2 } : { pose: 'stand' }), style: CAST.mama, handR: [80, -330], eyes: 'wide', brows: 'determined', mouth: mm || 'flat', seed: 400 }); paper(ctx, mx - 0.85 * 80, 1560 - 0.85 * 330 - 40, 0.55, -0.15 + Math.sin(t * 8) * 0.05); }
    }
    if (!dark(t)) { ctx.save(); ctx.globalAlpha = 0.08 + 0.04 * Math.sin(t * 9); ctx.fillStyle = '#7FB8FF'; ctx.fillRect(0, 860, W, H); ctx.restore(); }
    if (dark(t)) blackout(ctx, t, null);
  }
  function gag(ctx, t) {
    const a = t - ev.gag, pop = ease.outBack(clamp(a / 0.2), 2.6);
    if (EP === 6) { wide(ctx, t); ctx.save(); ctx.translate(540, 1250); ctx.scale(pop, pop); G.text(ctx, 'الكهرباء راحت!', 0, 0, { size: 120, align: 'center', color: '#F2C23B', stroke: '#0A0A12', strokeW: 14, lang: 'ar' }); ctx.restore(); G.text(ctx, '⚡', 540, 760, { size: 200, align: 'center', alpha: Math.floor(a * 6) % 2 ? 0.3 : 1 }); return; }
    const bg = { 3: '#2A0E14', 4: '#F6F0E2', 5: '#2B1E4A', 7: '#3FA89B' }[EP];
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    G.rays(ctx, 540, 960, { n: 28, r0: 150, r1: 1800, color: 'rgba(255,255,255,0.25)', lw: 14, seed: 7, spin: a * 0.5 });
    ctx.save(); ctx.translate(540, 900); ctx.scale(pop, pop);
    if (EP === 3) { router(ctx, 0, -120, 2.4, t); ctx.strokeStyle = '#E0503E'; ctx.lineWidth = 28; ctx.beginPath(); ctx.moveTo(-260, -360); ctx.lineTo(260, 120); ctx.moveTo(260, -360); ctx.lineTo(-260, 120); ctx.stroke(); G.text(ctx, 'انقطع النت!', 0, 330, { size: 120, align: 'center', color: '#FFFFFF', stroke: '#14121C', strokeW: 14, lang: 'ar' }); }
    if (EP === 4) { paper(ctx, 0, -60, 2.6, -0.06); G.text(ctx, '٤ / ١٠ 😱', 0, 470, { size: 120, align: 'center', color: '#D62E2E', stroke: '#14121C', strokeW: 12, lang: 'ar' }); }
    if (EP === 5) { G.text(ctx, 'WINNER', 0, -120, { size: 170, align: 'center', fam: 'Bungee', weight: 400, color: '#F2C23B', stroke: '#14121C', strokeW: 16 }); G.text(ctx, '🍗', 0, 180, { size: 260, align: 'center' }); for (let i = 0; i < 5; i++) star(ctx, -280 + i * 140, -380, 44, '#F2C23B'); }
    if (EP === 7) { for (let k = 0; k < 9; k++) { const ang = k * 0.7, d = a * 700; money(ctx, Math.cos(ang) * d * 0.6 + (k - 4) * 40, -100 + Math.sin(ang) * d * 0.4 - 200 * a + 400 * a * a, 0.9, 1, a * 6 + k); } G.text(ctx, 'راحت العيدية! 💸', 0, 420, { size: 110, align: 'center', color: '#FFFFFF', stroke: '#14121C', strokeW: 14, lang: 'ar' }); }
    ctx.restore();
  }
  function close(ctx, t, who) {
    room(ctx, t);
    const m = talk(who, t);
    if (who === 'hamoudi') {
      sofa(ctx, 540, 1900);
      const sad = EP === 7, scared = EP === 4;
      Ch.person(ctx, { x: 540, y: 1780, s: 1.9, pose: 'sit', style: CAST.hamoudi, eyes: sad ? 'normal' : 'wide', brows: 'worried', mouth: m || (sad ? 'wavy' : 'o'), gesture: scared ? 'shrug' : (EP === 3 || sad) ? null : 'point', handL: EP === 3 ? [-45, -95] : undefined, handR: EP === 3 ? [45, -95] : undefined, sweat: 0.9, seed: 300 });
      if (EP === 3) controller(ctx, 540, 1780 - 1.9 * 95, 1.3);
      if (sad) for (const sx of [-1, 1]) { const k = (t * 1.5) % 1; G.ellipse(ctx, 540 + sx * 70, 1780 - 1.9 * 360 + k * 120, 10, 16, { fill: '#7FC4E8', lw: 2, seed: 160 + sx }); }
    } else {
      const s = 2.0;
      Ch.person(ctx, { x: 540, y: 2120, s, pose: 'stand', style: CAST.mama, brows: EP === 5 ? 'up' : 'determined', eyes: EP === 5 ? 'happy' : 'normal', mouth: m || (EP === 5 ? 'grin' : 'flat'),
        handR: EP === 7 ? [150, -300] : EP === 5 ? [120, -470] : [130, -330], handL: EP === 6 ? [-120, -300] : [-90, -250], gesture: null, seed: 400 });
      if (EP === 3) router(ctx, 540 + s * 130, 2120 - s * 330 - 40, 1.2, t);
      if (EP === 4) { controller(ctx, 540 + s * 130, 2120 - s * 330, 1.2); paper(ctx, 540 - s * 90, 2120 - s * 250, 0.8, 0.2); }
      if (EP === 5) { headset(ctx, 540, 2120 - s * 310, s); controller(ctx, 540 - s * 90, 2120 - s * 250, 1.2); }
      if (EP === 6) { fan(ctx, 540 + s * 130, 2120 - s * 330, 1.3, t); candle(ctx, 540 - s * 120, 2120 - s * 300, 1.4, t); }
      if (EP === 7) { const u = clamp((t - (S.vo[1].at + 0.6)) / 0.5); if (t > ev.gag) money(ctx, 540 + s * 150, 2120 - s * 300 - 60, 1.0, 5, 0.2); }
      if (m && EP !== 5 && EP !== 7) for (let k = 0; k < 3; k++) G.line(ctx, [[250 + k * 30, 560 - k * 40], [210 + k * 30, 520 - k * 40]], { color: '#E0503E', lw: 9, seed: 95 + k });
    }
    if (dark(t)) blackout(ctx, t, who === 'mama' ? [540 - 2.0 * 120, 2120 - 2.0 * 300 - 200] : null, 0.6);
  }
  function endCard(ctx, t) {
    const e = clamp((t - ev.end) / 0.5); if (e <= 0) return;
    ctx.save(); ctx.globalAlpha = e; ctx.fillStyle = 'rgba(16,12,28,0.8)'; ctx.fillRect(0, 0, W, H);
    const pop = ease.outBack(e, 2); ctx.translate(540, 820); ctx.scale(pop, pop);
    G.text(ctx, 'حمودي وماما', 0, -80, { size: 140, align: 'center', color: '#F2C23B', stroke: '#1A1A22', strokeW: 14, lang: 'ar' });
    G.text(ctx, 'الجزء ' + EP + ': ' + S.TITLE, 0, 90, { size: 90, align: 'center', color: '#FFFFFF', lang: 'ar' });
    G.text(ctx, 'تابعنا للجزء ' + (EP + 1) + ' 👇', 0, 250, { size: 70, align: 'center', color: '#E8E4FF', lang: 'ar' });
    ctx.restore();
  }
  function caption(ctx, t) {
    for (const l of S.vo) if (t >= l.at && t < l.at + l.dur + 0.2) {
      const k = ease.outBack(clamp((t - l.at) / 0.2), 2);
      ctx.save(); ctx.translate(540, 935); ctx.scale(k, k);
      G.rrect(ctx, -510, -62, 1020, 96, 26, { fill: 'rgba(14,12,22,0.85)', lw: 0, seed: 99 });
      const size = l.text.length > 34 ? 42 : 50;
      G.text(ctx, l.text, 0, 0, { size, align: 'center', color: l.who === 'mama' ? '#FFD86B' : '#9FD4FF', lang: 'ar' });
      ctx.restore();
    }
  }
  // the episode badge in the first 2 seconds (the hook)
  function badge(ctx, t) { const a = clamp(1 - (t - 2) / 0.4); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; G.rrect(ctx, 300, 240, 480, 90, 45, { fill: '#E0503E', lw: 4, seed: 98 }); G.text(ctx, 'الجزء ' + EP + ' 🎮', 540, 302, { size: 54, align: 'center', color: '#FFFFFF', lang: 'ar' }); ctx.restore(); }

  const draws = { wide: (c, t) => wide(c, t), gag: (c, t) => gag(c, t), close: null };
  Studio.film({
    post: { vignette: 0.3, grain: 0.04, paper: 0.3 },
    fadeOut: 0.6,
    draw(ctx, t) {
      let i = 0; while (i + 1 < S.shots.length && t >= S.shots[i + 1].t0) i++;
      const sh = S.shots[i], local = t - sh.t0;
      const z = 1 + 0.04 * clamp(local / 4);
      const shake = sh.kind === 'gag' ? 22 * Math.exp(-local * 5) : 0;
      ctx.save(); ctx.translate(W / 2 + U.noise1(t * 30, 1) * shake, H / 2 + U.noise1(t * 30, 2) * shake); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
      if (sh.kind === 'close') close(ctx, t, sh.who); else draws[sh.kind](ctx, t);
      ctx.restore();
      const f = 1 - clamp(local / 0.12); if (i > 0 && f > 0) { ctx.fillStyle = `rgba(255,255,255,${0.7 * f})`; ctx.fillRect(0, 0, W, H); }
      if (t < ev.end) caption(ctx, t);
      if (EP !== 6 || t < ev.gag) badge(ctx, t);
      endCard(ctx, t);
    },
  });
})();
