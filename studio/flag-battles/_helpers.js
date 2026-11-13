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

  // ---- more countries (simplified) ----
  'عُمان': { t: 'h', c: ['#ffffff', '#db161b', '#008000'], lband: '#db161b', col: '#db161b' },
  'اليمن': { t: 'h', c: ['#ce1126', '#ffffff', '#000000'], col: '#ce1126' },
  'فلسطين': { t: 'h', c: ['#000000', '#ffffff', '#009736'], tri: '#ee2a35', col: '#009736' },
  'البحرين': { t: 'solid', c: ['#ce1126'], serr: '#ffffff', col: '#ce1126' },
  'ليبيا': { t: 'h', c: ['#e70013', '#000000', '#000000', '#239e46'], wcres: '#000000', col: '#239e46' },
  'السودان': { t: 'h', c: ['#d21034', '#ffffff', '#000000'], tri: '#007229', col: '#007229' },
  'تركيا': { t: 'solid', c: ['#e30a17'], wcres: '#e30a17', col: '#e30a17' },
  'الصين': { t: 'solid', c: ['#de2910'], cstar: '#ffde00', col: '#de2910' },
  'كوريا الجنوبية': { t: 'solid', c: ['#ffffff'], korea: 1, col: '#cd2e3a' },
  'الهند': { t: 'h', c: ['#ff9933', '#ffffff', '#138808'], wheel: '#000080', col: '#ff9933' },
  'أستراليا': { t: 'solid', c: ['#00008b'], wstars: '#ffffff', col: '#00008b' },
  'كندا': { t: 'v', c: ['#d52b1e', '#ffffff', '#ffffff', '#d52b1e'], leaf: '#d52b1e', col: '#d52b1e' },
  'نيجيريا': { t: 'v', c: ['#008751', '#ffffff', '#008751'], col: '#008751' },
  'غانا': { t: 'h', c: ['#ce1126', '#fcd116', '#006b3f'], star: '#000000', fstar: 1, col: '#fcd116' },
  'الكاميرون': { t: 'v', c: ['#007a5e', '#ce1126', '#fcd116'], star: '#fcd116', fstar: 1, col: '#007a5e' },
  'السنغال': { t: 'v', c: ['#00853f', '#fdef42', '#e31b23'], star: '#00853f', fstar: 1, col: '#00853f' },
  'كرواتيا': { t: 'h', c: ['#ff0000', '#ffffff', '#171796'], checks: 1, col: '#ff0000' },
  'بلجيكا': { t: 'v', c: ['#000000', '#fdda24', '#ef3340'], col: '#fdda24' },
  'السويد': { t: 'solid', c: ['#006aa7'], nordic: '#fecc00', col: '#006aa7' },
  'النرويج': { t: 'solid', c: ['#ba0c2f'], nordic: '#ffffff', nordic2: '#00205b', col: '#ba0c2f' },
  'أوروغواي': { t: 'h', c: ['#ffffff', '#0038a8', '#ffffff', '#0038a8', '#ffffff', '#0038a8', '#ffffff', '#0038a8', '#ffffff'], sunTL: '#fcd116', col: '#0038a8' },
  'كولومبيا': { t: 'h', c: ['#fcd116', '#fcd116', '#003893', '#ce1126'], col: '#fcd116' },
  // ---- football clubs: kit colours only (no crests) ----
  'ريال مدريد': { t: 'solid', c: ['#ffffff'], band: '#febe10', club: 1, col: '#febe10' },
  'برشلونة': { t: 'v', c: ['#a50044', '#004d98', '#a50044', '#004d98', '#a50044'], club: 1, col: '#a50044' },
  'مانشستر يونايتد': { t: 'solid', c: ['#da291c'], band: '#000000', club: 1, col: '#da291c' },
  'مانشستر سيتي': { t: 'solid', c: ['#6cabdd'], band: '#ffffff', club: 1, col: '#6cabdd' },
  'ليفربول': { t: 'solid', c: ['#c8102e'], collar: '#f6eb61', club: 1, col: '#c8102e' },
  'تشيلسي': { t: 'solid', c: ['#034694'], collar: '#ffffff', club: 1, col: '#034694' },
  'أرسنال': { t: 'v', c: ['#ffffff', '#ef0107', '#ef0107', '#ef0107', '#ffffff'], club: 1, col: '#ef0107' },
  'توتنهام': { t: 'h', c: ['#ffffff', '#ffffff', '#132257'], club: 1, col: '#132257' },
  'بايرن ميونخ': { t: 'h', c: ['#dc052d', '#ffffff', '#dc052d'], club: 1, col: '#dc052d' },
  'دورتموند': { t: 'solid', c: ['#fde100'], band: '#000000', club: 1, col: '#fde100' },
  'يوفنتوس': { t: 'v', c: ['#000000', '#ffffff', '#000000', '#ffffff', '#000000', '#ffffff'], club: 1, col: '#ffffff' },
  'ميلان': { t: 'v', c: ['#fb090b', '#000000', '#fb090b', '#000000', '#fb090b', '#000000'], club: 1, col: '#fb090b' },
  'إنتر': { t: 'v', c: ['#010e80', '#000000', '#010e80', '#000000', '#010e80', '#000000'], club: 1, col: '#0068a8' },
  'نابولي': { t: 'solid', c: ['#12a0d7'], collar: '#ffffff', club: 1, col: '#12a0d7' },
  'باريس سان جيرمان': { t: 'v', c: ['#004170', '#004170', '#ffffff', '#da291c', '#ffffff', '#004170', '#004170'], club: 1, col: '#004170' },
  'مارسيليا': { t: 'solid', c: ['#ffffff'], band: '#2faee0', club: 1, col: '#2faee0' },
  'أتلتيكو مدريد': { t: 'v', c: ['#cb3524', '#ffffff', '#cb3524', '#ffffff', '#cb3524', '#ffffff'], club: 1, col: '#cb3524' },
  'بوكا جونيورز': { t: 'h', c: ['#103f79', '#f3b229', '#103f79'], club: 1, col: '#f3b229' },
  'ريفر بليت': { t: 'solid', c: ['#ffffff'], sash: '#e30613', club: 1, col: '#e30613' },
  'الهلال': { t: 'solid', c: ['#005eb8'], collar: '#ffffff', club: 1, col: '#005eb8' },
  'النصر': { t: 'solid', c: ['#ffde00'], band: '#0a2a66', club: 1, col: '#ffde00' },
  'الاتحاد': { t: 'v', c: ['#fcd116', '#000000', '#fcd116', '#000000', '#fcd116', '#000000'], club: 1, col: '#fcd116' },
  'الأهلي السعودي': { t: 'solid', c: ['#006747'], band: '#ffffff', club: 1, col: '#006747' },
  'الأهلي': { t: 'solid', c: ['#e30613'], collar: '#ffffff', club: 1, col: '#e30613' },
  'الزمالك': { t: 'solid', c: ['#ffffff'], twin: '#e30613', club: 1, col: '#e30613' },
  'الوداد': { t: 'solid', c: ['#d71920'], band: '#ffffff', club: 1, col: '#d71920' },
  'الرجاء': { t: 'solid', c: ['#00843d'], band: '#ffffff', club: 1, col: '#00843d' },
  'الترجي': { t: 'h', c: ['#e2001a', '#fcd116', '#e2001a', '#fcd116', '#e2001a'], club: 1, col: '#fcd116' },
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
  if (f.star && !f.fstar) { g.strokeStyle = f.star; g.lineWidth = r * .07; g.beginPath(); for (let i = 0; i <= 5; i++) { const a = -Math.PI / 2 + i * 4 * Math.PI / 5; g.lineTo(x + Math.cos(a) * r * .38, y + Math.sin(a) * r * .38); } g.stroke(); }
  if (f.cres) { g.fillStyle = f.cres; g.beginPath(); g.arc(x, y, r * .32, 0, TAU); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(x + r * .1, y, r * .27, 0, TAU); g.fill(); }

  if (f.lband) { g.fillStyle = f.lband; g.fillRect(x0, y0, S * .3, S); }
  if (f.tri) { g.fillStyle = f.tri; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x0 + S * .45, y); g.lineTo(x0, y0 + S); g.fill(); }
  if (f.serr) { g.fillStyle = f.serr; g.beginPath(); g.moveTo(x0, y0); const n = 5; for (let i = 0; i <= n; i++) { g.lineTo(x0 + S * .3, y0 + i * S / n); if (i < n) g.lineTo(x0 + S * .45, y0 + (i + .5) * S / n); } g.lineTo(x0, y0 + S); g.closePath(); g.fill(); }
  if (f.wcres) { g.fillStyle = '#fff'; g.beginPath(); g.arc(x - r * .08, y, r * .34, 0, TAU); g.fill(); g.fillStyle = f.wcres; g.beginPath(); g.arc(x + r * .02, y, r * .28, 0, TAU); g.fill();
    g.fillStyle = '#fff'; g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .05 : r * .12; g.lineTo(x + r * .32 + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.closePath(); g.fill(); }
  if (f.cstar) { g.fillStyle = f.cstar; const st = (cx, cy, R) => { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? R * .4 : R; g.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); } g.closePath(); g.fill(); };
    st(x - r * .35, y - r * .3, r * .3); [[.05, -.6], [.2, -.4], [.2, -.1], [.05, .1]].forEach(([dx, dy]) => st(x + dx * r, y + dy * r, r * .09)); }
  if (f.korea) { g.fillStyle = '#cd2e3a'; g.beginPath(); g.arc(x, y, r * .38, Math.PI, TAU); g.fill(); g.fillStyle = '#0047a0'; g.beginPath(); g.arc(x, y, r * .38, 0, Math.PI); g.fill();
    g.fillStyle = '#000'; for (const [dx, dy] of [[-.62, -.5], [.62, -.5], [-.62, .5], [.62, .5]]) g.fillRect(x + dx * r - r * .1, y + dy * r - r * .08, r * .2, r * .16); }
  if (f.wheel) { g.strokeStyle = f.wheel; g.lineWidth = r * .04; g.beginPath(); g.arc(x, y, r * .2, 0, TAU); g.stroke(); for (let i = 0; i < 12; i++) { const a = i * TAU / 12; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * r * .2, y + Math.sin(a) * r * .2); g.stroke(); } }
  if (f.wstars) { g.fillStyle = '#fff'; const st = (cx, cy, R) => { g.beginPath(); for (let i = 0; i < 14; i++) { const a = -Math.PI / 2 + i * Math.PI / 7, rr = i % 2 ? R * .45 : R; g.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); } g.closePath(); g.fill(); };
    g.fillStyle = '#c8102e'; g.fillRect(x0, y0 + S * .22, S * .5, S * .06); g.fillRect(x0 + S * .22, y0, S * .06, S * .5); g.fillStyle = '#fff'; st(x - r * .45, y + r * .45, r * .16); [[.45, -.45], [.65, .05], [.25, .1], [.45, .6]].forEach(([dx, dy]) => st(x + dx * r, y + dy * r, r * .09)); }
  if (f.leaf) { g.fillStyle = f.leaf; g.beginPath(); g.moveTo(x, y - r * .4); g.lineTo(x + r * .3, y - r * .05); g.lineTo(x + r * .15, y + r * .02); g.lineTo(x + r * .22, y + r * .25); g.lineTo(x, y + r * .15); g.lineTo(x - r * .22, y + r * .25); g.lineTo(x - r * .15, y + r * .02); g.lineTo(x - r * .3, y - r * .05); g.closePath(); g.fill(); g.fillRect(x - r * .03, y + r * .1, r * .06, r * .25); }
  if (f.fstar) { g.fillStyle = f.star; g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .1 : r * .25; g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } g.closePath(); g.fill(); }
  if (f.checks) { const cs = r * .09; for (let i = -2; i < 3; i++) for (let j = -2; j < 3; j++) { g.fillStyle = (i + j) % 2 ? '#fff' : '#ff0000'; g.fillRect(x + i * cs - cs / 2, y + j * cs - cs / 2, cs, cs); } g.strokeStyle = '#171796'; g.lineWidth = 2; g.strokeRect(x - cs * 2.5, y - cs * 2.5, cs * 5, cs * 5); }
  if (f.nordic) { g.fillStyle = f.nordic; g.fillRect(x - r * .45, y0, r * .3, S); g.fillRect(x0, y - r * .15, S, r * .3); if (f.nordic2) { g.fillStyle = f.nordic2; g.fillRect(x - r * .38, y0, r * .16, S); g.fillRect(x0, y - r * .08, S, r * .16); } }
  if (f.sunTL) { g.fillStyle = f.sunTL; g.beginPath(); g.arc(x - r * .45, y - r * .45, r * .2, 0, TAU); g.fill(); }
  if (f.band) { g.fillStyle = f.band; g.fillRect(x0, y + r * .12, S, r * .2); }
  if (f.collar) { g.fillStyle = f.collar; g.beginPath(); g.moveTo(x - r * .35, y0); g.lineTo(x, y - r * .55); g.lineTo(x + r * .35, y0); g.lineTo(x + r * .2, y0); g.lineTo(x, y - r * .7); g.lineTo(x - r * .2, y0); g.closePath(); g.fill(); }
  if (f.sash) { g.strokeStyle = f.sash; g.lineWidth = r * .32; g.beginPath(); g.moveTo(x0, y0 + S); g.lineTo(x0 + S, y0); g.stroke(); }
  if (f.twin) { g.fillStyle = f.twin; g.fillRect(x0, y - r * .2, S, r * .12); g.fillRect(x0, y + r * .08, S, r * .12); }
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

