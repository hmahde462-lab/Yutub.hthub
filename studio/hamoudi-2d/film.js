// HAMOUDI & MAMA PART 2: every frame is a pure function of t.
(function () {
  const U = globalThis.U, G = globalThis.G, Ch = globalThis.Ch, Shots = globalThis.Shots, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev, T } = S;
  const W = G.W, H = G.H;
  const CAST = {
    mama: { outfit: 'abaya', robe: '#1F1D26', hairStyle: 'hijab', hijab: '#2B2833', skin: '#D2A07A', build: 'regular' },
    hamoudi: { outfit: 'tee', shirt: '#3C8DDB', bottoms: 'shorts', shorts: '#2E3A55', skin: '#D2A07A', hairStyle: 'short', hair: '#2A1D16', build: 'heavy' },
  };
  globalThis.CAST = CAST;
  const talk = (who, t) => { for (const l of S.vo) if (l.who === who && t >= l.at && t < l.at + l.dur - 0.05) { const a = t - l.at; const o = 0.25 + 0.6 * Math.abs(Math.sin(a * 13)) * (0.6 + 0.4 * Math.sin(a * 3.1)); return { open: o, wide: 0.5 + 0.3 * Math.sin(a * 7), talking: true }; } return null; };
  const starsAt = (t) => (t >= ev.six ? 6 : ev.stars.filter((s) => t >= s).length);
  const siren = (t) => t >= ev.six && t < ev.slipper + 3 ? (Math.floor((t - ev.six) * 4) % 2 ? '#E03A3A' : '#2F6BFF') : null;

  function star(ctx, x, y, r, fill) {
    const p = []; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.45 : r; p.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
    G.poly(ctx, p, { fill, lw: 3, seed: 40 + Math.round(x), step: 12 });
  }
  function controller(ctx, x, y, s) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    G.rrect(ctx, -70, -26, 140, 52, 24, { fill: '#2C2C34', lw: 4, seed: 70 });
    G.ellipse(ctx, -40, 0, 11, 11, { fill: '#55556A', lw: 2, seed: 71 }); G.ellipse(ctx, 40, -8, 7, 7, { fill: '#E0503E', lw: 2, seed: 72 }); G.ellipse(ctx, 54, 6, 7, 7, { fill: '#3FA89B', lw: 2, seed: 73 });
    ctx.restore();
  }
  function slipper(ctx, x, y, s, rot) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
    G.rrect(ctx, -32, -95, 64, 190, 30, { fill: '#2D7FD0', lw: 5, seed: 80 });
    G.rrect(ctx, -36, -40, 72, 34, 10, { fill: '#F2B84B', lw: 4, seed: 81 });
    ctx.restore();
  }
  // the game on the TV: a made-up night car chase
  function game(ctx, x, y, w, h, t) {
    ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    const on = t >= ev.play;
    ctx.fillStyle = on ? '#1C2340' : '#101018'; ctx.fillRect(x, y, w, h);
    if (!on) { G.text(ctx, 'PAUSE ⏸', x + w / 2, y + h / 2 + 20, { size: 70, align: 'center', fam: 'Bungee', weight: 400, color: '#8C8CA8' }); ctx.restore(); return; }
    const sp = t * 900;
    ctx.fillStyle = '#3A3A48'; ctx.beginPath(); ctx.moveTo(x + w * 0.42, y + h * 0.28); ctx.lineTo(x + w * 0.58, y + h * 0.28); ctx.lineTo(x + w + 60, y + h); ctx.lineTo(x - 60, y + h); ctx.fill();
    for (let k = 0; k < 7; k++) { const u = ((k / 7) + (sp / 2500)) % 1, yy = y + h * 0.28 + h * 0.72 * u * u; ctx.fillStyle = '#F2D08A'; ctx.fillRect(x + w / 2 - 4 - 10 * u, yy, 8 + 20 * u, 10 + 50 * u * u); }
    for (let k = 0; k < 6; k++) { const u = ((k / 6) + sp / 3000) % 1; ctx.fillStyle = '#26304F'; ctx.fillRect(x + w * 0.42 - w * 0.6 * u * u - 60 * u, y + h * 0.28 - 200 * u, 60 + 120 * u, 200 * u + 30); ctx.fillRect(x + w * 0.58 + w * 0.6 * u * u, y + h * 0.28 - 200 * u, 60 + 120 * u, 200 * u + 30); }
    // her car (orange) weaving
    const cx = x + w / 2 + Math.sin(t * 3.2) * w * 0.18, cy = y + h * 0.78;
    G.rrect(ctx, cx - 80, cy - 40, 160, 80, 18, { fill: '#F08A24', lw: 4, seed: 90 });
    G.rrect(ctx, cx - 55, cy - 70, 110, 40, 12, { fill: '#7FC4E8', lw: 4, seed: 91 });
    // police cars behind, more as stars rise
    const n = Math.min(4, starsAt(t));
    for (let i = 0; i < n; i++) {
      const px = x + w * (0.3 + 0.4 * ((i * 0.37) % 1)) + Math.sin(t * 2 + i) * 30, py = y + h * (0.45 + i * 0.05), s = 0.5 + i * 0.05;
      G.rrect(ctx, px - 70 * s, py - 30 * s, 140 * s, 60 * s, 10, { fill: '#F2F2F2', lw: 3, seed: 92 + i });
      ctx.fillStyle = Math.floor(t * 6 + i) % 2 ? '#E03A3A' : '#2F6BFF'; ctx.fillRect(px - 25 * s, py - 48 * s, 50 * s, 18 * s);
    }
    // the wanted stars
    const st = starsAt(t);
    for (let i = 0; i < 6; i++) {
      const lit = i < st, pop = lit ? ease.outBack(clamp((t - (i < 5 ? ev.stars[i] : ev.six)) / 0.25), 3) : 1;
      star(ctx, x + w - 45 - i * 62, y + 50, 26 * pop, lit ? (st === 6 && Math.floor(t * 6) % 2 ? '#FFFFFF' : '#F2C23B') : 'rgba(255,255,255,0.15)');
    }
    G.text(ctx, '$ 1,000,000', x + 30, y + 65, { size: 34, fam: 'Bungee', weight: 400, color: '#7CE07C' });
    ctx.restore();
  }
  function tv(ctx, t, glowOnly) {
    // the TV panel at the top (what mama sees)
    const x = 70, y = 230, w = 940, h = 600;
    G.rrect(ctx, x - 24, y - 24, w + 48, h + 48, 22, { fill: '#17171C', lw: 6, seed: 60 });
    game(ctx, x, y, w, h, t);
  }
  function room(ctx, t) {
    const sr = siren(t);
    ctx.fillStyle = '#3B3350'; ctx.fillRect(0, 0, W, H);
    G.rrect(ctx, -20, 0, W + 40, 1260, 0, { fill: '#5A4E78', lw: 0, seed: 1, hatch: { color: 'rgba(0,0,0,0.12)', gap: 16 } });
    // window with the moon
    G.rrect(ctx, 760, 900, 220, 260, 8, { fill: '#1A2244', lw: 5, seed: 2 }); G.ellipse(ctx, 900, 960, 30, 30, { fill: '#F6EFC8', lw: 2, seed: 3 });
    // floor + rug
    G.rrect(ctx, -20, 1260, W + 40, 700, 0, { fill: '#6E4E3A', lw: 4, seed: 4, hatch: { color: 'rgba(0,0,0,0.15)', gap: 14 } });
    G.ellipse(ctx, 540, 1700, 470, 120, { fill: '#9C2F3A', lw: 4, seed: 5, hatch: { color: 'rgba(242,184,75,0.4)', gap: 18 } });
    if (sr) { ctx.save(); ctx.globalAlpha = 0.22; ctx.fillStyle = sr; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  }
  function sofa(ctx, x, y) {
    G.rrect(ctx, x - 300, y - 230, 600, 170, 30, { fill: '#7A8C5A', lw: 5, seed: 20 });
    G.rrect(ctx, x - 340, y - 110, 680, 120, 26, { fill: '#8FA36A', lw: 5, seed: 21 });
    G.rrect(ctx, x - 360, y - 170, 70, 180, 24, { fill: '#7A8C5A', lw: 5, seed: 22 }); G.rrect(ctx, x + 290, y - 170, 70, 180, 24, { fill: '#7A8C5A', lw: 5, seed: 23 });
  }
  function zzz(ctx, x, y, t) { for (let i = 0; i < 3; i++) { const a = ((t * 0.7 + i / 3) % 1); ctx.save(); ctx.globalAlpha = 1 - a; G.text(ctx, 'z', x + a * 60 + i * 10, y - a * 160, { size: 40 + i * 14, fam: 'Bungee', weight: 400, color: '#E8E4FF' }); ctx.restore(); } }

  // wide: the living room, TV panel on top
  function wide(ctx, t, s) {
    room(ctx, t);
    tv(ctx, t);
    // Hamoudi asleep on the sofa (or gone in the outro)
    sofa(ctx, 540, 1330);
    const gone = t >= ev.outro;
    if (!gone) {
      Ch.person(ctx, { x: 470, y: 1250, s: 0.7, pose: 'sit', style: CAST.hamoudi, eyes: 'sleep', mouth: 'sleep', headRot: -0.25, pillow: 0.6, seed: 300 });
      if (t < ev.snatch) controller(ctx, 470, 1210, 0.55);
      if (t < ev.six) zzz(ctx, 520, 1000, t);
    } else {
      const w = Ch.walk(t, { x0: 470, speed: -520, t0: ev.outro, stride: 220 });
      if (w.x > -200) Ch.person(ctx, { x: w.x, y: 1450, s: 0.75, sx: -1, pose: 'walk', walk: Math.abs(w.walk), style: CAST.hamoudi, eyes: 'wide', mouth: 'o', brows: 'worried', sweat: 0.8, seed: 300 });
    }
    // mama: tiptoes in, snatches, sits on the cushion and plays
    const sitting = t >= ev.play - 0.15;
    G.ellipse(ctx, 540, 1690, 170, 40, { fill: '#E0A13E', lw: 4, seed: 30 });
    if (!sitting) {
      const u = clamp((t - ev.walkIn) / (ev.snatch - ev.walkIn));
      const x = lerp(1250, 600, ease.outQuad(u));
      Ch.person(ctx, { x, y: 1720, s: 0.95, sx: -1, ...(u < 1 ? { pose: 'walk', walk: t * 3.2 } : { pose: 'stand' }), style: CAST.mama, eyes: u < 1 ? 'normal' : 'happy', look: -0.6, mouth: 'smirk', brows: 'up', handR: t >= ev.snatch ? [60, -380] : null, seed: 400 });
      if (t >= ev.snatch) controller(ctx, x - 57, 1720 - 0.95 * 380, 0.6);
    } else {
      const lean = Math.sin(t * 3.2) * 0.08, hype = t >= ev.six;
      const m = talk('mama', t);
      Ch.person(ctx, { x: 540, y: 1680, s: 1.05, pose: 'sit', rot: lean, style: CAST.mama, handL: [-45, -95], handR: [45, -95], eyes: hype ? 'happy' : 'wide', brows: 'up', mouth: m || (hype ? 'grin' : 'smile'), lookY: -0.6, seed: 400 });
      controller(ctx, 540 + Math.sin(lean) * -100, 1680 - 1.05 * 95, 0.75);
      if (hype) G.confetti(ctx, t, ev.six, { n: 50, seed: 6 });
    }
    // TV light on the room
    if (t >= ev.play) { ctx.save(); ctx.globalAlpha = 0.08 + 0.04 * Math.sin(t * 9); ctx.fillStyle = '#7FB8FF'; ctx.fillRect(0, 860, W, H); ctx.restore(); }
  }
  // 6 STARS impact frame
  function six(ctx, t, s) {
    const a = t - ev.six;
    ctx.fillStyle = Math.floor(a * 6) % 2 ? '#E03A3A' : '#2F6BFF'; ctx.fillRect(0, 0, W, H);
    G.rays(ctx, 540, 900, { n: 30, r0: 140, r1: 1800, color: 'rgba(255,255,255,0.35)', lw: 14, seed: 7, spin: a * 0.6 });
    for (let i = 0; i < 6; i++) { const p = ease.outBack(clamp((a - i * 0.04) / 0.2), 3); star(ctx, 540 + (i - 2.5) * 150, 820 + (i % 2) * 40, 62 * p, '#F2C23B'); }
    const pop = ease.outBack(clamp(a / 0.2), 2.6);
    ctx.save(); ctx.translate(540, 1080); ctx.scale(pop, pop);
    G.text(ctx, '6 نجوم!', 0, 0, { size: 170, align: 'center', color: '#FFFFFF', stroke: '#1A1A22', strokeW: 16, lang: 'ar' });
    ctx.restore();
  }
  // Hamoudi wakes up
  function wake(ctx, t, s) {
    room(ctx, t);
    sofa(ctx, 540, 1900);
    const m = talk('hamoudi', t);
    const shock = ease.outBack(clamp((t - ev.wake) / 0.25), 2);
    Ch.person(ctx, { x: 540, y: 1780, s: 1.9, pose: 'sit', style: CAST.hamoudi, eyes: 'wide', brows: 'worried', mouth: m || 'o', gesture: t > ev.wake + 0.4 ? 'point' : null, headY: -20 * shock, sweat: 0.9, seed: 300 });
    if (t < ev.wake + 0.5) { ctx.save(); ctx.globalAlpha = 1 - clamp((t - ev.wake) / 0.5); G.text(ctx, '!!', 830, 700, { size: 160, fam: 'Bungee', weight: 400, color: '#F2C23B', stroke: '#1A1A22', strokeW: 12 }); ctx.restore(); }
  }
  // mama turns with the slipper
  function slip(ctx, t, s) {
    room(ctx, t);
    const a = t - ev.slipper, m = talk('mama', t);
    const raise = ease.outBack(clamp(a / 0.25), 2);
    G.rays(ctx, 540, 1000, { n: 24, r0: 200, r1: 1600, color: 'rgba(224,80,62,0.25)', lw: 18, seed: 9, spin: a * 0.3 });
    Ch.person(ctx, { x: 540, y: 2120, s: 2.1, pose: 'stand', style: CAST.mama, brows: 'determined', eyes: 'normal', mouth: m || 'flat', handR: [lerp(120, 140, raise), lerp(-300, -440, raise) + Math.sin(t * 14) * 10], handL: [-90, -250], seed: 400 });
    slipper(ctx, 540 + 2.1 * lerp(120, 140, raise), 2120 + 2.1 * (lerp(-300, -440, raise) + Math.sin(t * 14) * 10) - 110, 1.3, 0.3 + Math.sin(t * 14) * 0.06);
    controller(ctx, 540 - 2.1 * 90, 2120 - 2.1 * 250, 1.1);
    if (m) for (let k = 0; k < 3; k++) G.line(ctx, [[250 + k * 30, 560 - k * 40], [210 + k * 30, 520 - k * 40]], { color: '#E0503E', lw: 9, seed: 95 + k });
  }
  // the end card
  function endCard(ctx, t) {
    const e = clamp((t - ev.end) / 0.5); if (e <= 0) return;
    ctx.save(); ctx.globalAlpha = e; ctx.fillStyle = 'rgba(16,12,28,0.78)'; ctx.fillRect(0, 0, W, H);
    const pop = ease.outBack(e, 2); ctx.translate(540, 820); ctx.scale(pop, pop);
    G.text(ctx, 'حمودي وماما', 0, -60, { size: 140, align: 'center', color: '#F2C23B', stroke: '#1A1A22', strokeW: 14, lang: 'ar' });
    G.text(ctx, 'الجزء 2 🎮', 0, 110, { size: 110, align: 'center', color: '#FFFFFF', lang: 'ar' });
    G.text(ctx, 'تابعنا للجزء 3 👇', 0, 280, { size: 70, align: 'center', color: '#E8E4FF', lang: 'ar' });
    ctx.restore();
  }
  function caption(ctx, t) {
    for (const l of S.vo) if (t >= l.at && t < l.at + l.dur + 0.2) {
      const k = ease.outBack(clamp((t - l.at) / 0.2), 2);
      ctx.save(); ctx.translate(540, 935); ctx.scale(k, k);
      G.rrect(ctx, -500, -62, 1000, 96, 26, { fill: 'rgba(14,12,22,0.82)', lw: 0, seed: 99 });
      G.text(ctx, l.text, 0, 0, { size: 50, align: 'center', color: l.who === 'mama' ? '#FFD86B' : '#9FD4FF', lang: 'ar' });
      ctx.restore();
    }
  }
  const film = Shots.film([
    { at: 0, draw: wide, cam: Shots.push(1, 1.04) },
    { at: ev.six, draw: six, in: 'flash', cam: Shots.shake(26, ev.six, 5) },
    { at: ev.wake, draw: wake, in: 'cut', cam: Shots.combine(Shots.shake(14, ev.wake, 6), Shots.push(1, 1.06)) },
    { at: ev.slipper, draw: slip, in: 'whip', cam: Shots.shake(16, ev.slipper, 6) },
    { at: ev.outro, draw: wide, in: 'cut' },
  ]);
  Studio.film({
    post: { vignette: 0.3, grain: 0.04, paper: 0.3 },
    fadeOut: 0.6,
    draw(ctx, t) { film(ctx, t); if (t < ev.end) caption(ctx, t); endCard(ctx, t); },
  });
})();
