const FLAG = {
  'العراق': { t: 'h', c: ['#ce1126', '#ffffff', '#000000'], mark: '#007a3d', col: '#ce1126' },
  'البرازيل': { t: 'brazil', col: '#009c3b' }, 'السعودية': { t: 'solid', c: ['#006c35'], bar: '#ffffff', col: '#006c35' },
  'الأرجنتين': { t: 'h', c: ['#74acdf', '#ffffff', '#74acdf'], sun: '#f6b40e', col: '#74acdf' },
  'مصر': { t: 'h', c: ['#ce1126', '#ffffff', '#000000'], eagle: '#c09300', col: '#c09300' },
  'إسبانيا': { t: 'h', c: ['#aa151b', '#f1bf00', '#f1bf00', '#aa151b'], col: '#f1bf00' },
  'المغرب': { t: 'solid', c: ['#c1272d'], star: '#006233', col: '#c1272d' },
  'البرتغال': { t: 'v', c: ['#006600', '#006600', '#ff0000', '#ff0000', '#ff0000'], col: '#ff0000' },
  'الجزائر': { t: 'v', c: ['#006233', '#ffffff'], cres: '#d21034', col: '#006233' },
  'فرنسا': { t: 'v', c: ['#0055a4', '#ffffff', '#ef4135'], col: '#0055a4' },
  'ألمانيا': { t: 'h', c: ['#000000', '#dd0000', '#ffce00'], col: '#ffce00' },
  'اليابان': { t: 'solid', c: ['#ffffff'], disc: '#bc002d', col: '#bc002d' },
  'إنجلترا': { t: 'solid', c: ['#ffffff'], cross: '#ce1124', col: '#ffffff' },
  'إيطاليا': { t: 'v', c: ['#009246', '#ffffff', '#ce2b37'], col: '#009246' },
  'هولندا': { t: 'h', c: ['#ae1c28', '#ffffff', '#21468b'], col: '#ff7f00' },
  'أمريكا': { t: 'usa', col: '#3c3b6e' },
  'الأردن': { t: 'jordan', col: '#007a3d' }, 'الكويت': { t: 'kuwait', col: '#007a3d' },
  'الإمارات': { t: 'uae', col: '#00732f' }, 'قطر': { t: 'qatar', col: '#8a1538' },
  'سوريا': { t: 'h', c: ['#ce1126', '#ffffff', '#000000'], stars2: '#007a3d', col: '#ce1126' },
  'لبنان': { t: 'h', c: ['#ed1c24', '#ffffff', '#ffffff', '#ed1c24'], cedar: '#00a651', col: '#00a651' },
  'تونس': { t: 'solid', c: ['#e70013'], disc: '#ffffff', cres: '#e70013', col: '#e70013' },
  'المكسيك': { t: 'v', c: ['#006847', '#ffffff', '#ce1126'], eagle: '#8b5a2b', col: '#006847' },
};
const font = (px, fam = 'Lalezar') => `${fam === 'Cairo' ? '900 ' : ''}${px}px '${fam}'`;
function text(s, x, y, px, col, o = {}) { g.font = font(px, o.fam); const mw = o.max ?? 1800, w0 = g.measureText(s).width; if (w0 > mw) { px = Math.floor(px * mw / w0); g.font = font(px, o.fam); }
  g.textAlign = o.align || 'center'; g.textBaseline = 'middle'; g.direction = 'rtl'; g.lineJoin = 'round'; if (o.stroke !== 0) { g.lineWidth = o.stroke ?? 9; g.strokeStyle = '#000'; g.strokeText(s, x, y); } g.fillStyle = col; g.fillText(s, x, y); }
function flagBall(name, x, y, r, glow = 0) { const f = FLAG[name];
  if (glow) { g.save(); g.shadowColor = f.col; g.shadowBlur = glow; g.fillStyle = f.col; g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill(); g.restore(); }
  g.save(); g.beginPath(); g.arc(x, y, r, 0, TAU); g.clip(); const x0 = x - r, y0 = y - r, S = 2 * r;
  if (f.t === 'h') f.c.forEach((c, i) => { g.fillStyle = c; g.fillRect(x0, y0 + i * S / f.c.length, S, S / f.c.length + 1); });
  else if (f.t === 'v') f.c.forEach((c, i) => { g.fillStyle = c; g.fillRect(x0 + i * S / f.c.length, y0, S / f.c.length + 1, S); });
  else if (f.t === 'solid') { g.fillStyle = f.c[0]; g.fillRect(x0, y0, S, S); }
  else if (f.t === 'brazil') { g.fillStyle = '#009c3b'; g.fillRect(x0, y0, S, S); g.fillStyle = '#ffdf00'; g.beginPath(); g.moveTo(x - r * .85, y); g.lineTo(x, y - r * .6); g.lineTo(x + r * .85, y); g.lineTo(x, y + r * .6); g.fill(); g.fillStyle = '#002776'; g.beginPath(); g.arc(x, y, r * .33, 0, TAU); g.fill(); }
  else if (f.t === 'usa') { for (let i = 0; i < 9; i++) { g.fillStyle = i % 2 ? '#ffffff' : '#b22234'; g.fillRect(x0, y0 + i * S / 9, S, S / 9 + 1); } g.fillStyle = '#3c3b6e'; g.fillRect(x0, y0, S * .5, S * .5); g.fillStyle = '#fff'; for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) { g.beginPath(); g.arc(x0 + S * (.1 + i * .15), y0 + S * (.1 + j * .15), r * .05, 0, TAU); g.fill(); } }
  if (f.t === 'jordan' || f.t === 'kuwait' || f.t === 'uae') { const cs = f.t === 'jordan' ? ['#000000', '#ffffff', '#007a3d'] : f.t === 'kuwait' ? ['#007a3d', '#ffffff', '#ce1126'] : ['#00732f', '#ffffff', '#000000'];
    cs.forEach((c, i) => { g.fillStyle = c; g.fillRect(x0, y0 + i * S / 3, S, S / 3 + 1); });
    if (f.t === 'jordan') { g.fillStyle = '#ce1126'; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x0 + S * .55, y); g.lineTo(x0, y0 + S); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(x0 + S * .2, y, r * .07, 0, TAU); g.fill(); }
    else if (f.t === 'kuwait') { g.fillStyle = '#000'; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x0 + S * .3, y0 + S / 3); g.lineTo(x0 + S * .3, y0 + 2 * S / 3); g.lineTo(x0, y0 + S); g.fill(); }
    else { g.fillStyle = '#ff0000'; g.fillRect(x0, y0, S * .27, S); } }
  else if (f.t === 'qatar') { g.fillStyle = '#8a1538'; g.fillRect(x0, y0, S, S); g.fillStyle = '#fff'; g.beginPath(); g.moveTo(x0, y0); const n = 9; for (let i = 0; i <= n; i++) { g.lineTo(x0 + S * .3, y0 + (i + .5) * S / (n + 1) - S / (2 * (n + 1))); g.lineTo(x0 + S * .42, y0 + (i + .5) * S / (n + 1)); } g.lineTo(x0 + S * .3, y0 + S); g.lineTo(x0, y0 + S); g.closePath(); g.fill(); }
  if (f.stars2) { g.fillStyle = f.stars2; for (const sd of [-1, 1]) { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .06 : r * .15; g.lineTo(x + sd * r * .3 + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.closePath(); g.fill(); } }
  if (f.cedar) { g.fillStyle = f.cedar; g.beginPath(); g.moveTo(x, y - r * .3); g.lineTo(x + r * .3, y + r * .22); g.lineTo(x - r * .3, y + r * .22); g.closePath(); g.fill(); g.fillRect(x - r * .04, y + r * .2, r * .08, r * .12); }
  if (f.mark) { g.fillStyle = f.mark; for (let i = -1; i <= 1; i++) { g.beginPath(); g.arc(x + i * r * .22, y, r * .07, 0, TAU); g.fill(); } }
  if (f.eagle) { g.fillStyle = f.eagle; g.beginPath(); g.arc(x, y, r * .14, 0, TAU); g.fill(); }
  if (f.bar) { g.fillStyle = f.bar; g.fillRect(x - r * .5, y + r * .3, r, r * .08); }
  if (f.sun) { g.fillStyle = f.sun; g.beginPath(); g.arc(x, y, r * .13, 0, TAU); g.fill(); }
  if (f.disc) { g.fillStyle = f.disc; g.beginPath(); g.arc(x, y, r * .45, 0, TAU); g.fill(); }
  if (f.cross) { g.fillStyle = f.cross; g.fillRect(x - r * .13, y0, r * .26, S); g.fillRect(x0, y - r * .13, S, r * .26); }
  if (f.star) { g.strokeStyle = f.star; g.lineWidth = r * .07; g.beginPath(); for (let i = 0; i <= 5; i++) { const a = -Math.PI / 2 + i * 4 * Math.PI / 5; g.lineTo(x + Math.cos(a) * r * .38, y + Math.sin(a) * r * .38); } g.stroke(); }
  if (f.cres) { g.fillStyle = f.cres; g.beginPath(); g.arc(x, y, r * .32, 0, TAU); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(x + r * .1, y, r * .27, 0, TAU); g.fill(); }
  const sh = g.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r * 1.05); sh.addColorStop(0, 'rgba(255,255,255,.45)'); sh.addColorStop(.5, 'rgba(255,255,255,0)'); sh.addColorStop(1, 'rgba(0,0,0,.35)'); g.fillStyle = sh; g.fillRect(x0, y0, S, S);
  g.restore(); g.strokeStyle = 'rgba(0,0,0,.75)'; g.lineWidth = Math.max(2, r * .07); g.beginPath(); g.arc(x, y, r, 0, TAU); g.stroke(); }
function eyes(x, y, r, look, mood) { g.fillStyle = '#fff'; g.strokeStyle = '#000'; g.lineWidth = 2;
  for (const sd of [-1, 1]) { g.beginPath(); g.ellipse(x + sd * r * .3, y - r * .05, r * .17, r * .21, 0, 0, TAU); g.fill(); g.stroke(); }
  g.fillStyle = '#111'; for (const sd of [-1, 1]) { g.beginPath(); g.arc(x + sd * r * .3 + Math.cos(look) * r * .07, y - r * .03 + Math.sin(look) * r * .06, r * .085, 0, TAU); g.fill(); }
  if (mood) { g.strokeStyle = '#000'; g.lineWidth = r * .08; g.lineCap = 'round'; for (const sd of [-1, 1]) { g.beginPath(); g.moveTo(x + sd * r * .12, y - r * .3); g.lineTo(x + sd * r * .48, y - r * .42); g.stroke(); } } }
const ICON = { sword: '⚔️', knife: '🔪', axe: '🪓', hammer: '🔨', spear: '🔱', saw: '⚙️', heal: '🧪', shield: '🛡️', bomb: '💣', speed: '⚡' };
const WNAME = { sword: 'سيف', knife: 'سكين', axe: 'فأس', hammer: 'مطرقة', spear: 'رمح', saw: 'منشار', heal: 'علاج', shield: 'درع', bomb: 'قنبلة', speed: 'سرعة' };


function arenaPath(s, R) { const C = s.cfg; g.beginPath(); if (C.sides) { for (let k = 0; k < C.sides; k++) { const a = C.rot + k * TAU / C.sides; g.lineTo(C.cx + Math.cos(a) * R, C.cy + Math.sin(a) * R); } g.closePath(); } else g.arc(C.cx, C.cy, R, 0, TAU); }
function drawWeapon(s, b) { const w = b.w; if (!w) return; const G = s.weaponGeom(b); g.lineCap = 'round';
  if (G.disc) { g.save(); g.translate(G.x, G.y); g.rotate(s.t * 18); g.fillStyle = '#c0c8d0'; g.strokeStyle = '#2b3036'; g.lineWidth = 3; g.beginPath(); for (let i = 0; i < 24; i++) { const a = i * Math.PI / 12, r = i % 2 ? G.rad * .78 : G.rad; g.lineTo(Math.cos(a) * r, Math.sin(a) * r); } g.closePath(); g.fill(); g.stroke(); g.restore(); return; }
  const ux = Math.cos(G.ang), uy = Math.sin(G.ang), px = -uy, py = ux;
  if (w.type === 'sword' || w.type === 'knife') { const bw = w.type === 'sword' ? 11 : 9; g.strokeStyle = '#4a2c14'; g.lineWidth = 12; g.beginPath(); g.moveTo(G.ax, G.ay); g.lineTo(G.ax + ux * 20, G.ay + uy * 20); g.stroke();
    const sx = G.ax + ux * 20, sy = G.ay + uy * 20; g.fillStyle = '#e4ebf2'; g.strokeStyle = '#3a4048'; g.lineWidth = 3; g.beginPath(); g.moveTo(sx + px * bw, sy + py * bw); g.lineTo(G.bx - ux * 18 + px * bw * .7, G.by - uy * 18 + py * bw * .7); g.lineTo(G.bx, G.by); g.lineTo(G.bx - ux * 18 - px * bw * .7, G.by - uy * 18 - py * bw * .7); g.lineTo(sx - px * bw, sy - py * bw); g.closePath(); g.fill(); g.stroke();
    if (w.type === 'sword') { g.strokeStyle = '#d9a52b'; g.lineWidth = 9; g.beginPath(); g.moveTo(sx + px * 24, sy + py * 24); g.lineTo(sx - px * 24, sy - py * 24); g.stroke(); } }
  else if (w.type === 'axe' || w.type === 'hammer') { g.strokeStyle = '#7a4a22'; g.lineWidth = 11; g.beginPath(); g.moveTo(G.ax, G.ay); g.lineTo(G.bx, G.by); g.stroke(); const hx = G.bx - ux * 14, hy = G.by - uy * 14;
    g.fillStyle = w.type === 'axe' ? '#a9b2bb' : '#59606a'; g.strokeStyle = '#1d2126'; g.lineWidth = 4; g.beginPath();
    if (w.type === 'axe') { g.moveTo(hx - px * 8, hy - py * 8); g.lineTo(hx + px * 40 - ux * 14, hy + py * 40 - uy * 14); g.quadraticCurveTo(hx + px * 52 + ux * 10, hy + py * 52 + uy * 10, hx + px * 36 + ux * 22, hy + py * 36 + uy * 22); g.lineTo(hx - px * 8 + ux * 10, hy - py * 8 + uy * 10); }
    else { g.moveTo(hx - px * 30 - ux * 16, hy - py * 30 - uy * 16); g.lineTo(hx + px * 30 - ux * 16, hy + py * 30 - uy * 16); g.lineTo(hx + px * 30 + ux * 16, hy + py * 30 + uy * 16); g.lineTo(hx - px * 30 + ux * 16, hy - py * 30 + uy * 16); }
    g.closePath(); g.fill(); g.stroke(); }
  else if (w.type === 'spear') { g.strokeStyle = '#8a5a2e'; g.lineWidth = 9; g.beginPath(); g.moveTo(G.ax, G.ay); g.lineTo(G.bx - ux * 24, G.by - uy * 24); g.stroke(); g.fillStyle = '#dfe6ee'; g.strokeStyle = '#2b3036'; g.lineWidth = 3; g.beginPath(); g.moveTo(G.bx, G.by); g.lineTo(G.bx - ux * 34 + px * 13, G.by - uy * 34 + py * 13); g.lineTo(G.bx - ux * 26, G.by - uy * 26); g.lineTo(G.bx - ux * 34 - px * 13, G.by - uy * 34 - py * 13); g.closePath(); g.fill(); g.stroke(); } }

