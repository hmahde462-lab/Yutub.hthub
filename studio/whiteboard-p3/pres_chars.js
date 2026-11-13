(function(){
// Stickman character + scenery drawing helpers (flat 2D, round white heads).
const TAU = Math.PI * 2;
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const seg = (u, a, b) => clamp((u - a) / (b - a));
const ease = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const easeOut = x => 1 - Math.pow(1 - clamp(x), 3);
function rng(seed) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }

const INK = '#141414';
const CHARS = {
  saleem:   { robe: '#5fb7f0', vest: '#8a5a2b', sash: '#ffffff', turban: '#ffffff', band: '#5fb7f0', beard: true, scale: 1 },
  abu:      { robe: '#2f7d3b', sash: '#e8322b', cap: '#7a1f2b', mustache: true, fat: true, scale: 1 },
  governor: { robe: '#7a3fc4', trim: '#f2c230', sash: '#f2c230', turban: '#ffffff', bigTurban: true, gem: '#e8322b', beard: true, beardColor: '#9a9a9a', scale: 1.05 },
};
const EXTRA_COLORS = ['#e07a2f', '#c94f8a', '#3f8fd1', '#9c7a3c', '#5aa86b', '#d1b33f', '#8a6fd1', '#d15b4f'];

/* pose: x,y (feet), s scale, armL/armR angles (rad from straight down, + = outward), cross, walk (phase), bob,
   tilt, look (-1..1 head turn), eyes: dot|wide|squint|closed|wink, brows: calm|up|angry|sad|oneUp, mouth: line|smile|open|laugh|o|frown, talk (0..1), lean */
function drawChar(g, spec, p) {
  const s = (p.s || 1) * (spec.scale || 1);
  g.save(); g.translate(p.x, p.y - (p.bob || 0)); g.rotate(p.lean || 0); g.scale(s, s);
  g.lineCap = 'round'; g.lineJoin = 'round';
  const legLen = 62, robeTop = -212, robeBot = -44, hipY = -60;
  // legs
  const w = p.walk || 0, step = Math.sin(w) * 14;
  g.strokeStyle = INK; g.lineWidth = 7;
  for (const [sx, k] of [[-12, 1], [12, -1]]) {
    g.beginPath(); g.moveTo(sx, hipY); g.lineTo(sx + step * k, 0); g.stroke();
    g.fillStyle = INK; g.beginPath(); g.ellipse(sx + step * k + 6 * Math.sign(sx || 1), 0, 11, 6, 0, 0, TAU); g.fill();
  }
  // robe (bean / long gown)
  const fat = spec.fat ? 16 : 0, topW = 40 + fat, botW = 50 + fat * 1.2;
  g.fillStyle = spec.robe; g.strokeStyle = INK; g.lineWidth = 6;
  g.beginPath(); g.moveTo(-topW, robeTop + 26); g.quadraticCurveTo(-topW, robeTop, -topW + 26, robeTop); g.lineTo(topW - 26, robeTop);
  g.quadraticCurveTo(topW, robeTop, topW, robeTop + 26); g.quadraticCurveTo(botW + 6, (robeTop + robeBot) / 2, botW, robeBot);
  g.quadraticCurveTo(0, robeBot + 10, -botW, robeBot); g.quadraticCurveTo(-botW - 6, (robeTop + robeBot) / 2, -topW, robeTop + 26); g.closePath(); g.fill(); g.stroke();
  if (spec.trim) { g.strokeStyle = spec.trim; g.lineWidth = 6; g.beginPath(); g.moveTo(0, robeTop + 4); g.lineTo(0, robeBot + 4); g.stroke(); }
  if (spec.vest) { g.fillStyle = spec.vest; for (const sd of [-1, 1]) { g.beginPath(); g.moveTo(sd * 8, robeTop + 2); g.lineTo(sd * (topW - 4), robeTop + 10); g.lineTo(sd * (topW + 2), robeTop + 92); g.lineTo(sd * 14, robeTop + 92); g.closePath(); g.fill(); } }
  g.fillStyle = spec.sash; g.fillRect(-topW - 3, robeTop + 92, (topW + 3) * 2, 16); g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(-topW - 3, robeTop + 92, (topW + 3) * 2, 16);
  g.fillStyle = INK; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(0, robeTop + 28 + i * 20, 3.2, 0, TAU); g.fill(); }
  // arms
  const shY = robeTop + 22, armLen = 82;
  const hand = (hx, hy) => { g.fillStyle = '#fff'; g.strokeStyle = INK; g.lineWidth = 5; g.beginPath(); g.arc(hx, hy, 10, 0, TAU); g.fill(); g.stroke(); };
  g.strokeStyle = INK; g.lineWidth = 7;
  if (p.cross) {
    for (const sd of [-1, 1]) { g.beginPath(); g.moveTo(sd * topW, shY); g.lineTo(sd * (topW - 6), shY + 40); g.lineTo(-sd * 20, shY + 34); g.stroke(); }
    hand(-22, shY + 32); hand(22, shY + 36);
  } else {
    p._hands = [];
    for (const [sd, ang] of [[-1, p.armL ?? .15], [1, p.armR ?? .15]]) {
      const a = ang, hx = sd * topW + sd * Math.sin(a) * armLen, hy = shY + Math.cos(a) * armLen;
      g.strokeStyle = INK; g.lineWidth = 7; g.beginPath(); g.moveTo(sd * topW, shY); g.lineTo(hx, hy); g.stroke(); hand(hx, hy);
      p._hands.push([hx, hy]);
    }
  }
  // head
  const R = 52, hy = robeTop - R + 6;
  g.save(); g.translate(0, hy); g.rotate(p.tilt || 0);
  g.fillStyle = '#fff'; g.strokeStyle = INK; g.lineWidth = 6; g.beginPath(); g.arc(0, 0, R, 0, TAU); g.fill(); g.stroke();
  const lk = (p.look || 0) * 12;
  if (spec.beard) { g.fillStyle = spec.beardColor || INK; g.beginPath(); g.arc(lk * .5, 4, R - 3, .18 * Math.PI, .82 * Math.PI); g.quadraticCurveTo(lk * .5, R + 10, Math.cos(.18 * Math.PI) * (R - 3) + lk * .5, Math.sin(.18 * Math.PI) * (R - 3) + 4); g.fill(); }
  // eyes
  const ex = 17, ey = -6, eyes = p.eyes || 'dot';
  g.fillStyle = INK; g.strokeStyle = INK; g.lineWidth = 5;
  for (const sd of [-1, 1]) {
    const x = sd * ex + lk, y = ey;
    if (eyes === 'squint' || (eyes === 'wink' && sd === 1)) { g.beginPath(); g.moveTo(x - 8, y + 2); g.quadraticCurveTo(x, y - 7, x + 8, y + 2); g.stroke(); }
    else if (eyes === 'closed') { g.beginPath(); g.moveTo(x - 8, y); g.lineTo(x + 8, y); g.stroke(); }
    else { const r = eyes === 'wide' ? 9 : 6; g.beginPath(); g.ellipse(x, y, r * .8, r, 0, 0, TAU); g.fill();
      if (eyes === 'wide') { g.fillStyle = '#fff'; g.beginPath(); g.arc(x + 2, y - 3, 2.5, 0, TAU); g.fill(); g.fillStyle = INK; } }
  }
  // brows: inner end toward the face centre
  const br = p.brows || 'calm'; g.lineWidth = 6; g.strokeStyle = INK;
  for (const sd of [-1, 1]) {
    const x = sd * ex + lk; let yi = -25, yo = -25;
    if (br === 'up') { yi = yo = -34; }
    if (br === 'oneUp' && sd === 1) { yi = -34; yo = -38; }
    if (br === 'angry') { yi = -17; yo = -29; }
    if (br === 'sad') { yi = -31; yo = -20; }
    g.beginPath(); g.moveTo(x - sd * 11, yi); g.lineTo(x + sd * 11, yo); g.stroke();
  }
  if (spec.mustache) { g.fillStyle = INK; g.beginPath(); g.ellipse(lk - 12, 14, 14, 6, .25, 0, TAU); g.ellipse(lk + 12, 14, 14, 6, -.25, 0, TAU); g.fill(); }
  // mouth
  const m = p.mouth || 'line', talk = p.talk || 0, my = 26;
  g.strokeStyle = INK; g.fillStyle = '#3a0d0d'; g.lineWidth = 5;
  if (talk > 0.01 || m === 'open') { const o = m === 'open' ? 1 : talk; g.beginPath(); g.ellipse(lk, my, 12, 3 + 10 * o, 0, 0, TAU); g.fill(); g.stroke(); }
  else if (m === 'smile') { g.beginPath(); g.arc(lk, my - 10, 14, .2 * Math.PI, .8 * Math.PI); g.stroke(); }
  else if (m === 'laugh') { g.beginPath(); g.moveTo(lk - 18, my - 4); g.quadraticCurveTo(lk, my + 26, lk + 18, my - 4); g.closePath(); g.fill(); g.stroke(); }
  else if (m === 'o') { g.beginPath(); g.ellipse(lk, my + 2, 8, 11, 0, 0, TAU); g.fill(); g.stroke(); }
  else if (m === 'frown') { g.beginPath(); g.arc(lk, my + 12, 12, 1.2 * Math.PI, 1.8 * Math.PI); g.stroke(); }
  else { g.beginPath(); g.moveTo(lk - 11, my); g.lineTo(lk + 11, my); g.stroke(); }
  // headwear
  if (spec.turban) {
    const big = spec.bigTurban ? 1.25 : 1;
    g.fillStyle = spec.turban; g.strokeStyle = INK; g.lineWidth = 5;
    g.beginPath(); g.ellipse(0, -R + 6, 46 * big, 26 * big, 0, Math.PI, TAU); g.quadraticCurveTo(46 * big, -R + 14, 0, -R + 16); g.quadraticCurveTo(-46 * big, -R + 14, -46 * big, -R + 6); g.fill(); g.stroke();
    g.beginPath(); g.ellipse(0, -R - 14 * big, 30 * big, 20 * big, 0, 0, TAU); g.fill(); g.stroke();
    if (spec.band) { g.strokeStyle = spec.band; g.lineWidth = 6; g.beginPath(); g.ellipse(0, -R + 4, 44, 9, 0, 0, Math.PI); g.stroke(); }
    if (spec.gem) { g.fillStyle = spec.gem; g.strokeStyle = INK; g.lineWidth = 3; g.beginPath(); g.arc(0, -R - 2, 7, 0, TAU); g.fill(); g.stroke(); }
  }
  if (spec.cap) { g.save(); g.rotate(p.capTilt || 0); g.fillStyle = spec.cap; g.strokeStyle = INK; g.lineWidth = 5; g.beginPath(); g.arc(0, -R + 10, 30, Math.PI, TAU); g.closePath(); g.fill(); g.stroke(); g.restore(); }
  if (p.extraHead) p.extraHead(g, R);
  g.restore();
  g.restore();
  // world-space hand positions for props
  if (p._hands) p.hands = p._hands.map(([hx, hy]) => [p.x + hx * s, p.y - (p.bob || 0) + hy * s]);
  return p;
}
function extraSpec(i) { return { robe: EXTRA_COLORS[i % EXTRA_COLORS.length], sash: '#f4e6c8', turban: i % 3 === 0 ? null : '#ffffff', cap: i % 3 === 0 ? '#6b4a2b' : null, beard: i % 2 === 0, scale: 1 }; }
const laughPose = (x, y, t, k, s = 1) => ({ x, y, s, bob: Math.abs(Math.sin(t * 9 + k)) * 14, eyes: 'squint', brows: 'up', mouth: 'laugh', armL: .5 + .3 * Math.sin(t * 9 + k), armR: 2.4 + .2 * Math.sin(t * 9 + k), lean: Math.sin(t * 4.5 + k) * .06 });

// ---------- scenery ----------
function sky(g, stops, w = 1080, h = 1920, y0 = 0) { const gr = g.createLinearGradient(0, y0, 0, y0 + h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(-2000, y0, w + 4000, h); }
function sun(g, x, y, r, core, glow) { const gr = g.createRadialGradient(x, y, r * .3, x, y, r * 2.4); gr.addColorStop(0, glow); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r * 2.4, 0, TAU); g.fill(); g.fillStyle = core; g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill(); }
function dunes(g, y, cols) { cols.forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.moveTo(-1500, y + i * 60 + 400); for (let x = -1500; x <= 2600; x += 120) g.quadraticCurveTo(x + 60, y + i * 60 - 40 - 30 * Math.sin(x * .01 + i), x + 120, y + i * 60 + 10 * Math.cos(x * .02 + i)); g.lineTo(2600, y + 3000); g.lineTo(-1500, y + 3000); g.fill(); g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 3; g.stroke(); }); }
function palm(g, x, y, h, lean, s = 1) { g.save(); g.translate(x, y); g.strokeStyle = '#7a4a1e'; g.lineCap = 'round'; g.lineWidth = 22 * s; g.beginPath(); g.moveTo(0, 0); g.quadraticCurveTo(lean * h * .2, -h * .6, lean * h * .3, -h); g.stroke(); const tx = lean * h * .3, ty = -h; g.fillStyle = '#2f9e44'; g.strokeStyle = INK; g.lineWidth = 3;
  for (const a of [-2.8, -2.2, -1.6, -1.0, -0.4, -3.4]) { const L = 150 * s; g.beginPath(); g.moveTo(tx, ty); g.quadraticCurveTo(tx + Math.cos(a) * L * .5, ty + Math.sin(a) * L * .5 - 30 * s, tx + Math.cos(a) * L, ty + Math.sin(a) * L * .4 + 50 * s); g.quadraticCurveTo(tx + Math.cos(a) * L * .45, ty + Math.sin(a) * L * .45 + 6, tx, ty); g.fill(); g.stroke(); } g.restore(); }
function iceBlock(g, x, y, w, h, glow = 0) { g.save(); if (glow) { g.shadowColor = '#bfefff'; g.shadowBlur = 30 * glow; } g.fillStyle = '#bfe9ff'; g.strokeStyle = '#3d8fbf'; g.lineWidth = 4; g.beginPath(); g.roundRect(x - w / 2, y - h / 2, w, h, 8); g.fill(); g.stroke(); g.shadowBlur = 0; g.fillStyle = 'rgba(255,255,255,.85)'; g.beginPath(); g.roundRect(x - w / 2 + 8, y - h / 2 + 7, w * .35, 7, 3); g.fill(); g.restore(); }
function coin(g, x, y, r = 12, spin = 0) { g.fillStyle = '#ffd23b'; g.strokeStyle = '#a07400'; g.lineWidth = 3; g.beginPath(); g.ellipse(x, y, r * Math.abs(Math.cos(spin)) + 2, r, 0, 0, TAU); g.fill(); g.stroke(); }
window.SM={drawChar,CHARS,INK};})();
