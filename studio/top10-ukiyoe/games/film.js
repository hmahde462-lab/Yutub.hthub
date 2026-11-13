// TOP 10 IRAQI FOODS — ukiyo-e woodblock look. Every frame is a pure function of t.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev, items, vo } = S;
  const W = G.W, H = G.H;
  const C = {
    paper: '#EBDDBC', paper2: '#E2CFA6', ink: '#1C1A17', indigo: '#1E3557', prussian: '#2E5C8A', sky: '#9DBCD0',
    red: '#C2412D', ochre: '#D8A548', sage: '#7E8E5A', brown: '#7A4E2D', dark: '#4A3322', pink: '#E7B8A0', cream: '#F4EAD2', purple: '#5B3A5E', green: '#5E7A3A',
  };
  const AR = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  const arNum = (n) => String(n).split('').map((d) => AR[+d]).join('');
  const R = (i, k) => G.rnd(i, k); // deterministic 0..1

  // ---------- primitives in the woodblock manner: flat fills, firm ink lines ----------
  const ell = (ctx, x, y, rx, ry, fill, seed, lw = 4) => G.ellipse(ctx, x, y, rx, ry, { fill, lw, seed, amp: 0.25 });
  const poly = (ctx, pts, fill, seed, lw = 4) => G.poly(ctx, pts, { fill, lw, seed, step: 30, amp: 0.25 });
  const rr = (ctx, x, y, w, h, r, fill, seed, lw = 4) => G.rrect(ctx, x, y, w, h, r, { fill, lw, seed, amp: 0.25 });
  const ln = (ctx, pts, color, lw, seed) => G.line(ctx, pts, { color, lw, seed, amp: 0.25 });

  function sky(ctx) {
    ctx.fillStyle = C.paper; ctx.fillRect(0, 0, W, H);
    const g = ctx.createLinearGradient(0, 0, 0, 340); // bokashi: the printed blue fading into paper
    g.addColorStop(0, C.prussian); g.addColorStop(1, 'rgba(46,92,138,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, 340);
  }
  function sun(ctx, x, y, r) { ell(ctx, x, y, r, r, C.red, 5, 0); }
  function cloud(ctx, x, y, w, seed) { // kasumi: a long rounded band of mist
    rr(ctx, x, y, w, 46, 23, C.cream, seed, 3);
    rr(ctx, x + w * 0.2, y - 30, w * 0.5, 40, 20, C.cream, seed + 1, 3);
  }
  function clouds(ctx, t, y0 = 170) {
    for (let i = 0; i < 4; i++) { const w = 380 + R(i, 1) * 300, x = ((R(i, 2) * W + t * (12 + i * 5)) % (W + w + 200)) - w - 100; cloud(ctx, x, y0 + i * 70 + R(i, 3) * 40, w, 30 + i * 3); }
  }
  function malwiya(ctx, x, y, s, fill = C.sky) { // the spiral minaret of Samarra, as a distant silhouette
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    poly(ctx, [[-110, 0], [110, 0], [34, -360], [-34, -360]], fill, 50, 3);
    for (let k = 0; k < 5; k++) { const yy = -40 - k * 66, w = 100 - k * 16; ln(ctx, [[-w, yy + 28], [w, yy]], C.ink, 2.5, 51 + k); }
    rr(ctx, -22, -400, 44, 44, 6, fill, 56, 3);
    ctx.restore();
  }
  function palm(ctx, x, y, s, seed, fill = C.green) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ln(ctx, [[0, 0], [8, -120], [18, -240]], C.dark, 10, seed);
    for (let k = 0; k < 7; k++) { const a = -Math.PI / 2 + (k - 3) * 0.42, ex = 18 + Math.cos(a) * 130, ey = -240 + Math.sin(a) * 70 + Math.abs(k - 3) * 22; poly(ctx, [[18, -240], [ex, ey], [18 + Math.cos(a) * 70, -248 + Math.sin(a) * 30]], fill, seed + k, 2.5); }
    ctx.restore();
  }
  // the Tigris in Hokusai's manner: banded waves with curling foam claws
  function waves(ctx, y0, t, { color = C.prussian, amp = 26, len = 220, speed = 40, seed = 0, foam = true } = {}) {
    const ph = t * speed + seed * 97;
    const yAt = (x) => y0 + amp * Math.sin((x + ph) / len * Math.PI * 2) + amp * 0.35 * Math.sin((x + ph * 1.7) / (len * 0.47));
    ctx.beginPath(); ctx.moveTo(-20, H + 20);
    for (let x = -20; x <= W + 20; x += 12) ctx.lineTo(x, yAt(x));
    ctx.lineTo(W + 20, H + 20); ctx.closePath();
    ctx.fillStyle = color; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = C.ink; ctx.stroke();
    // inner bands
    ctx.save(); ctx.strokeStyle = 'rgba(234,221,188,0.45)'; ctx.lineWidth = 3;
    for (const d of [22, 44]) { ctx.beginPath(); for (let x = -20; x <= W + 20; x += 12) { const y = yAt(x) + d; x < 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke(); }
    ctx.restore();
    if (!foam) return;
    // foam claws at the crests
    const first = Math.floor((-ph) / len) - 1;
    for (let k = first; k < first + W / len + 3; k++) {
      const xc = k * len - ph + len * 0.75; // crest of the main sine
      if (xc < -60 || xc > W + 60) continue;
      const yc = yAt(xc);
      for (let j = 0; j < 4; j++) { const a = -0.4 + j * 0.45; ell(ctx, xc + 18 + Math.cos(a) * 26, yc - 6 + Math.sin(a) * 14, 7, 7, C.cream, 200 + k * 7 + j, 2); }
      ctx.save(); ctx.strokeStyle = C.cream; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(xc + 8, yc + 4, 16, Math.PI * 1.1, Math.PI * 2.2); ctx.stroke(); ctx.restore();
    }
  }
  function guffa(ctx, x, y, t) { // the round reed boat of the Tigris, with a fisherman
    const b = Math.sin(t * 1.6) * 6;
    ctx.save(); ctx.translate(x, y + b); ctx.rotate(Math.sin(t * 1.2) * 0.03);
    ell(ctx, 0, 0, 120, 34, C.dark, 70); ell(ctx, 0, -8, 104, 20, C.brown, 71, 3);
    // the man: a flat silhouette with a red keffiyeh
    poly(ctx, [[-20, -10], [22, -10], [16, -110], [-14, -110]], C.indigo, 72, 3);
    ell(ctx, 0, -130, 22, 24, C.pink, 73, 3);
    poly(ctx, [[-26, -136], [26, -136], [30, -100], [-30, -100]], C.red, 74, 3);
    ln(ctx, [[16, -90], [120, -230]], C.dark, 6, 75); // the oar / pole
    ctx.restore();
  }
  function steam(ctx, x, y, t, n = 3, h = 220, seed = 0) {
    for (let i = 0; i < n; i++) {
      const pts = []; const off = (i - (n - 1) / 2) * 60;
      for (let k = 0; k <= 12; k++) { const u = k / 12; pts.push([x + off + Math.sin(u * 6 + t * 2 + i) * 22 * u, y - u * h]); }
      ctx.save(); ctx.globalAlpha = 0.75; ln(ctx, pts, C.cream, 7, seed + i); ctx.restore();
    }
  }
  function plate(ctx, x, y, rx = 340, ry = 120) { // Imari-style plate: indigo rim with a wave pattern
    ell(ctx, x, y + 14, rx + 10, ry + 8, C.dark, 80);
    ell(ctx, x, y, rx, ry, C.indigo, 81);
    ctx.save(); ctx.strokeStyle = C.cream; ctx.lineWidth = 3;
    for (let k = 0; k < 22; k++) { const a = (k / 22) * Math.PI * 2; ctx.beginPath(); ctx.arc(x + Math.cos(a) * (rx - 22), y + Math.sin(a) * (ry - 10), 8, Math.PI, 0); ctx.stroke(); }
    ctx.restore();
    ell(ctx, x, y, rx - 48, ry - 26, C.cream, 82, 3);
  }
  function bowl(ctx, x, y, w, h, fill = C.indigo, inside = C.brown) {
    poly(ctx, [[x - w, y], [x + w, y], [x + w * 0.7, y + h], [x - w * 0.7, y + h]], fill, 90);
    ell(ctx, x, y, w, h * 0.28, inside, 91);
    ctx.save(); ctx.strokeStyle = C.cream; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x - w * 0.8, y + h * 0.45); ctx.lineTo(x + w * 0.8, y + h * 0.45); ctx.stroke(); ctx.restore();
  }

  // ---------- the ten dishes (drawn around 0,0 = middle of the plate) ----------
  const FOOD = {
    10(ctx, t) { // endless runner: rails in perspective, a train, coins, a sneaker
      poly(ctx, [[-120, -200], [120, -200], [380, 150], [-380, 150]], '#8A7A66', 1000);
      for (const sx of [-1, 1]) ln(ctx, [[sx * 60, -200], [sx * 230, 150]], C.ink, 6, 1001 + sx);
      for (let k = 0; k < 6; k++) { const u = ((k / 6) + t * 0.6) % 1, y = -200 + 350 * u * u, w = 70 + 170 * u * u; ln(ctx, [[-w, y], [w, y]], C.dark, 4 + 4 * u, 1005 + k); }
      rr(ctx, -330, -260, 170, 260, 18, C.ochre, 1010); rr(ctx, -310, -230, 130, 80, 10, C.sky, 1011, 3); ell(ctx, -280, -40, 16, 16, C.cream, 1012, 3); ell(ctx, -190, -40, 16, 16, C.cream, 1013, 3);
      for (let i = 0; i < 5; i++) { const y = -150 + i * 55 + Math.sin(t * 4 + i) * 6; ell(ctx, 40, y, 22, 22, '#E8C23A', 1020 + i, 3); }
      ctx.save(); ctx.translate(200, 40 + Math.abs(Math.sin(t * 4)) * -40); ctx.rotate(-0.2);
      poly(ctx, [[-90, 0], [70, 0], [100, 40], [-90, 40]], C.red, 1030); poly(ctx, [[-90, 0], [-60, -60], [0, -50], [70, 0]], C.red, 1031); ln(ctx, [[-50, -30], [20, -20]], C.cream, 4, 1032);
      ctx.restore();
    },
    9(ctx, t) { // village builder: walls, a tower, gold
      ell(ctx, 0, 110, 400, 90, C.sage, 1040);
      for (let i = 0; i < 8; i++) rr(ctx, -330 + i * 84, 30, 76, 60, 6, '#9A8F80', 1041 + i, 3);
      rr(ctx, -80, -220, 160, 260, 8, '#B9A27A', 1050); poly(ctx, [[-110, -220], [110, -220], [0, -330]], C.red, 1051);
      rr(ctx, -30, -60, 60, 100, 26, C.dark, 1052, 3);
      poly(ctx, [[0, -330], [0, -390], [60, -370], [0, -350]], C.red, 1053, 3);
      for (let i = 0; i < 8; i++) ell(ctx, 220 + (i % 4) * 34 - (i > 3 ? 17 : 0), 60 - (i > 3 ? 26 : 0), 24, 14, '#E8C23A', 1060 + i, 3);
      ell(ctx, -250, -40, 60, 38, C.dark, 1070); rr(ctx, -250, -60, 90, 26, 10, C.dark, 1071, 3); // cannon
    },
    8(ctx, t) { // block builder: isometric cubes + a pickaxe
      const cube = (x, y, s, top, side, seed) => { poly(ctx, [[x, y - s], [x + s, y - s / 2], [x, y], [x - s, y - s / 2]], top, seed, 3); poly(ctx, [[x - s, y - s / 2], [x, y], [x, y + s], [x - s, y + s / 2]], side, seed + 1, 3); poly(ctx, [[x + s, y - s / 2], [x, y], [x, y + s], [x + s, y + s / 2]], Ch_shade(side), seed + 2, 3); };
      const L = [[-160, 60], [0, 140], [160, 60], [0, -20], [-160, -100], [0, -180]];
      L.forEach(([x, y], i) => cube(x, y + Math.sin(t * 2 + i) * 4, 80, i % 3 === 2 ? C.sky : C.green, i % 3 === 1 ? '#8E8E8E' : '#8A5A32', 1080 + i * 3));
      ctx.save(); ctx.translate(290, -120); ctx.rotate(0.6 + Math.sin(t * 3) * 0.1); ln(ctx, [[0, 0], [0, 260]], C.dark, 16, 1100); poly(ctx, [[-120, -10], [120, -10], [70, 30], [-70, 30]], C.sky, 1101); ctx.restore();
    },
    7(ctx, t) { // shooter: a helmet, a crosshair, dog tags
      ell(ctx, -60, 20, 210, 170, C.sage, 1110); rr(ctx, -290, 40, 460, 50, 20, '#5E6E44', 1111);
      for (let k = 0; k < 5; k++) ln(ctx, [[-200 + k * 70, -100], [-180 + k * 70, 30]], '#5E6E44', 4, 1112 + k);
      ctx.save(); ctx.translate(250, -60); ctx.rotate(t * 0.5);
      ctx.strokeStyle = C.red; ctx.lineWidth = 9; ctx.beginPath(); ctx.arc(0, 0, 100, 0, Math.PI * 2); ctx.stroke(); ctx.beginPath(); ctx.arc(0, 0, 50, 0, Math.PI * 2); ctx.stroke();
      for (let k = 0; k < 4; k++) { ctx.save(); ctx.rotate(k * Math.PI / 2); ctx.beginPath(); ctx.moveTo(0, -140); ctx.lineTo(0, -70); ctx.stroke(); ctx.restore(); }
      ctx.restore();
      rr(ctx, 180, 110, 70, 100, 18, '#C0C0C0', 1120, 3); ln(ctx, [[215, 110], [180, 40], [250, 40], [215, 110]], C.dark, 3, 1121);
    },
    6(ctx, t) { // a light battle game on an old phone
      rr(ctx, -150, -260, 300, 520, 40, C.dark, 1130); rr(ctx, -125, -220, 250, 420, 16, C.indigo, 1131, 3);
      ln(ctx, [[-130, -40], [60, -200]], 'rgba(244,234,210,0.7)', 4, 1132); ln(ctx, [[-60, 120], [120, -60]], 'rgba(244,234,210,0.7)', 4, 1133); // the cracks
      for (let i = 0; i < 7; i++) { const x = -100 + i * 34, f = 50 * Math.sin(t * 7 + i * 1.3); poly(ctx, [[x - 30, 180], [x + 30, 180], [x + 6 + f * 0.2, 0 - f], [x - 4, 60]], i % 2 ? C.red : C.ochre, 1140 + i, 3); }
      ell(ctx, 0, 230, 18, 18, '#555', 1150, 3);
      rr(ctx, 210, 30, 140, 120, 10, '#8A5A32', 1155); ln(ctx, [[210, 90], [350, 90]], C.dark, 4, 1156); // a supply crate
    },
    5(ctx, t) { // battle-builder: wooden ramps and walls + a dance
      for (let k = 0; k < 3; k++) { poly(ctx, [[-360 + k * 120, 120 - k * 110], [-240 + k * 120, 120 - k * 110], [-120 + k * 120, 10 - k * 110], [-240 + k * 120, 10 - k * 110]], '#B07A3A', 1160 + k); for (let j = 0; j < 3; j++) ln(ctx, [[-330 + k * 120 + j * 35, 115 - k * 110], [-210 + k * 120 + j * 35, 5 - k * 110]], C.dark, 3, 1170 + k * 3 + j); }
      rr(ctx, 80, -160, 230, 280, 6, '#9A8F80', 1180); for (let r = 0; r < 4; r++) ln(ctx, [[80, -160 + r * 70], [310, -160 + r * 70]], C.dark, 3, 1181 + r);
      const b = Math.sin(t * 8) * 14; // music notes for the victory dance
      for (let i = 0; i < 3; i++) { const x = 380 + i * 50, y = -200 - i * 60 + (i % 2 ? b : -b); ell(ctx, x, y, 18, 14, C.red, 1190 + i, 3); ln(ctx, [[x + 16, y], [x + 16, y - 70]], C.ink, 4, 1195 + i); }
    },
    4(ctx, t) { // arena brawler: a trophy + a big star
      poly(ctx, [[-140, -220], [140, -220], [100, -40], [-100, -40]], '#E8C23A', 1200);
      ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 8; ctx.beginPath(); ctx.arc(-150, -150, 50, Math.PI * 0.5, Math.PI * 1.5); ctx.stroke(); ctx.beginPath(); ctx.arc(150, -150, 50, -Math.PI * 0.5, Math.PI * 0.5); ctx.stroke(); ctx.restore();
      rr(ctx, -30, -40, 60, 100, 6, '#C9A23A', 1201); rr(ctx, -120, 60, 240, 60, 8, C.dark, 1202);
      const s = 1 + 0.08 * Math.sin(t * 5);
      const p = []; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = (i % 2 ? 45 : 110) * s; p.push([300 + Math.cos(a) * r, -150 + Math.sin(a) * r]); } poly(ctx, p, C.red, 1210);
      const q = []; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = (i % 2 ? 24 : 60); q.push([-320 + Math.cos(a) * r, -60 + Math.sin(a) * r]); } poly(ctx, q, C.sky, 1211);
    },
    3(ctx, t) { // open-world crime: a car, a police light, six wanted stars
      const x = Math.sin(t * 2) * 30;
      rr(ctx, -280 + x, -40, 460, 120, 30, '#F08A24', 1220); poly(ctx, [[-180 + x, -40], [-120 + x, -130], [60 + x, -130], [120 + x, -40]], '#F08A24', 1221);
      poly(ctx, [[-160 + x, -46], [-112 + x, -116], [-30 + x, -116], [-30 + x, -46]], C.sky, 1222, 3); poly(ctx, [[-10 + x, -46], [-10 + x, -116], [50 + x, -116], [96 + x, -46]], C.sky, 1223, 3);
      ell(ctx, -170 + x, 90, 50, 50, C.ink, 1224); ell(ctx, 90 + x, 90, 50, 50, C.ink, 1225); ell(ctx, -170 + x, 90, 20, 20, '#999', 1226, 0); ell(ctx, 90 + x, 90, 20, 20, '#999', 1227, 0);
      rr(ctx, 260, -20, 120, 50, 10, Math.floor(t * 4) % 2 ? C.red : '#2F6BFF', 1230);
      for (let i = 0; i < 6; i++) { const p = []; for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + k * Math.PI / 5, r = k % 2 ? 14 : 32; p.push([-250 + i * 80 + Math.cos(a) * r, -260 + Math.sin(a) * r]); } poly(ctx, p, '#E8C23A', 1240 + i, 3); }
    },
    2(ctx, t) { // football: a ball on the pitch, a controller, and a glass of Iraqi tea
      poly(ctx, [[-380, 120], [380, 120], [300, -120], [-300, -120]], C.green, 1250);
      ln(ctx, [[0, -120], [0, 120]], C.cream, 4, 1251); ctx.save(); ctx.strokeStyle = C.cream; ctx.lineWidth = 4; ctx.beginPath(); ctx.ellipse(0, 0, 90, 40, 0, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
      const by = -Math.abs(Math.sin(t * 3)) * 80;
      ell(ctx, -60, -40 + by, 56, 56, C.cream, 1252); poly(ctx, [[-60, -64 + by], [-38, -48 + by], [-46, -22 + by], [-74, -22 + by], [-82, -48 + by]], C.ink, 1253, 2);
      rr(ctx, 120, 100, 220, 80, 36, C.dark, 1254); ell(ctx, 170, 140, 14, 14, '#666', 1255, 2); ell(ctx, 290, 130, 9, 9, C.red, 1256, 2); ell(ctx, 310, 150, 9, 9, C.sky, 1257, 2);
      // istikan: the slim tea glass on a saucer
      ell(ctx, -300, 170, 60, 14, C.cream, 1260, 3); poly(ctx, [[-330, 60], [-270, 60], [-284, 115], [-278, 165], [-322, 165], [-316, 115]], '#B4442A', 1261, 3);
      steam(ctx, -300, 50, t, 2, 120, 1262);
    },
    1(ctx, t) { // battle royale: a level-three helmet, a parachute, a frying pan and the chicken dinner
      ctx.save(); ctx.translate(-250, -150 + Math.sin(t * 1.5) * 12);
      poly(ctx, [[-130, 0], [-90, -70], [0, -95], [90, -70], [130, 0]], C.red, 1270); for (let k = -2; k <= 2; k++) ln(ctx, [[k * 50, -85 + Math.abs(k) * 15], [k * 50 * 0.5, 0]], C.cream, 3, 1271 + k);
      for (const sx of [-1, 1]) ln(ctx, [[sx * 128, 0], [0, 140]], C.ink, 2.5, 1276 + sx); rr(ctx, -30, 130, 60, 50, 8, '#8A5A32', 1278, 3);
      ctx.restore();
      ell(ctx, 40, 0, 150, 120, '#5E6E44', 1280); rr(ctx, -110, 40, 300, 50, 16, '#4C5A36', 1281); rr(ctx, -40, -20, 160, 60, 16, C.ink, 1282, 3); // helmet + visor
      ctx.save(); ctx.translate(300, 60); ctx.rotate(-0.5 + Math.sin(t * 4) * 0.1); ell(ctx, 0, 0, 90, 90, '#3A3A3A', 1290); ell(ctx, 0, 0, 70, 70, '#555', 1291, 3); rr(ctx, -16, 80, 32, 160, 10, C.dark, 1292); ctx.restore();
      // the chicken dinner on a plate
      plate(ctx, -180, 170, 160, 50); ell(ctx, -180, 140, 70, 40, '#B0612A', 1295); ell(ctx, -120, 112, 18, 18, C.cream, 1296, 3);
    },
  };
  const Ch_shade = (hex) => { const n = parseInt(hex.slice(1), 16); const f = 0.75; return '#' + [16, 8, 0].map((s) => Math.round(((n >> s) & 255) * f).toString(16).padStart(2, '0')).join(''); };

  // ---------- the red hanko seal with the number ----------
  function seal(ctx, x, y, s, n, rot = 0) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
    rr(ctx, -90, -90, 180, 180, 14, C.red, 600 + n, 5);
    ctx.strokeStyle = C.cream; ctx.lineWidth = 6; ctx.strokeRect(-72, -72, 144, 144);
    G.text(ctx, arNum(n), 0, 38, { size: 120, align: 'center', color: C.cream, lang: 'ar', weight: 700 });
    ctx.restore();
  }
  const fit = (ctx, str, size, maxW, fam, weight) => { const w = G.measure(ctx, str, size, fam, weight, 'ar'); return w > maxW ? size * maxW / w : size; };
  // the cartouche: a tall paper label on the right, like the title slip of a print
  function cartouche(ctx, it, t) {
    const k = ease.outCubic(clamp((t - it.at) / 0.6));
    const x = W - 560, y = 150, w = 470, h = 700;
    ctx.save(); ctx.translate(0, (1 - k) * -60); ctx.globalAlpha = k;
    rr(ctx, x - 10, y - 10, w + 20, h + 20, 6, C.ink, 700, 0);
    rr(ctx, x, y, w, h, 4, C.cream, 701, 3);
    ctx.strokeStyle = C.red; ctx.lineWidth = 4; ctx.strokeRect(x + 18, y + 18, w - 36, h - 36);
    seal(ctx, x + w / 2, y + 150, 0.9, it.n, -0.05);
    const big = fit(ctx, it.ar, 96, w - 70, undefined, 700);
    G.text(ctx, it.ar, x + w / 2, y + 380, { size: big, align: 'center', color: C.ink, lang: 'ar', weight: 700 });
    G.text(ctx, it.en.toUpperCase(), x + w / 2, y + 460, { size: 34, align: 'center', color: C.prussian, fam: 'Bungee', weight: 400 });
    ln(ctx, [[x + 70, y + 500], [x + w - 70, y + 500]], C.red, 3, 702);
    G.text(ctx, it.tag, x + w / 2, y + 580, { size: fit(ctx, it.tag, 44, w - 70), align: 'center', color: C.dark, lang: 'ar' });
    ctx.restore();
  }
  // a hand-print reveal: the dish is "printed" from left to right
  function printed(ctx, t0, t, x0, x1, fn) {
    const p = ease.inOutQuad(clamp((t - t0) / 0.8));
    ctx.save(); ctx.beginPath(); ctx.rect(x0, 0, (x1 - x0) * p, H); ctx.clip(); fn(); ctx.restore();
  }

  // ---------- scenes ----------
  function landscape(ctx, t, { sunX = 1500, sunY = 300, boat = true } = {}) {
    sky(ctx); sun(ctx, sunX, sunY, 120); clouds(ctx, t);
    malwiya(ctx, 380, 760, 1.1);
    palm(ctx, 120, 790, 1.2, 60); palm(ctx, 650, 780, 0.9, 61); palm(ctx, 1750, 790, 1.1, 62); palm(ctx, 1240, 785, 0.8, 63);
    rr(ctx, -20, 760, W + 40, 60, 0, C.sage, 64, 3);
    waves(ctx, 830, t, { color: C.sky, amp: 14, len: 260, speed: 25, seed: 1, foam: false });
    if (boat) guffa(ctx, 1000 + Math.sin(t * 0.2) * 120, 900, t);
    waves(ctx, 940, t, { color: C.prussian, amp: 24, len: 230, speed: 45, seed: 2 });
    waves(ctx, 1010, t, { color: C.indigo, amp: 30, len: 300, speed: 70, seed: 3 });
  }
  function titleCard(ctx, t) {
    landscape(ctx, t);
    // the title cartouche
    const k = ease.outBack(clamp((t - ev.title) / 0.5), 1.6);
    ctx.save(); ctx.translate(W / 2, 400); ctx.scale(k, k);
    rr(ctx, -560, -190, 1120, 330, 8, C.ink, 800, 0);
    rr(ctx, -548, -178, 1096, 306, 6, C.cream, 801, 3);
    ctx.strokeStyle = C.red; ctx.lineWidth = 5; ctx.strokeRect(-525, -155, 1050, 260);
    G.text(ctx, 'أكثر ١٠ ألعاب يحبها العراقيين', 0, -20, { size: fit(ctx, 'أكثر ١٠ ألعاب يحبها العراقيين', 120, 1000, undefined, 700), align: 'center', color: C.ink, lang: 'ar', weight: 700 });
    G.text(ctx, 'TOP 10 GAMES IRAQIS LOVE · UKIYO-E', 0, 70, { size: 40, align: 'center', color: C.prussian, fam: 'Bungee', weight: 400 });
    ctx.restore();
    seal(ctx, W / 2 + 470, 540, 0.75 * k, 10, 0.08);
  }
  function intro(ctx, t) { // the panorama while the intro is spoken
    landscape(ctx, t);
    const a = clamp((t - vo[0].at) / 1);
    G.text(ctx, 'من كهاوي بغداد… بعيون يابانية', W / 2, 260, { size: 80, align: 'center', color: C.ink, lang: 'ar', weight: 700, alpha: a });
  }
  function stampScene(ctx, t, it) { // the big seal slams in between dishes
    sky(ctx); clouds(ctx, t, 260);
    waves(ctx, 880, t, { color: C.prussian, amp: 26, len: 230, speed: 45, seed: 4 });
    waves(ctx, 980, t, { color: C.indigo, amp: 32, len: 300, speed: 70, seed: 5 });
    const hit = it.stamp + 0.35, a = t - hit;
    const s = a < 0 ? lerp(3.2, 1.3, ease.inQuad(clamp((t - it.stamp) / 0.35))) : 1.3 * (1 + 0.08 * Math.exp(-a * 10));
    seal(ctx, W / 2, 470, s, it.n, -0.06);
    if (a >= 0) {
      for (let i = 0; i < 12; i++) { const ang = (i / 12) * Math.PI * 2, r = 200 + a * 500; ctx.save(); ctx.globalAlpha = Math.max(0, 1 - a * 2); ln(ctx, [[W / 2 + Math.cos(ang) * r, 470 + Math.sin(ang) * r], [W / 2 + Math.cos(ang) * (r + 60), 470 + Math.sin(ang) * (r + 60)]], C.ink, 6, 900 + i); ctx.restore(); }
      G.text(ctx, it.n === 1 ? 'رقم واحد!' : 'رقم ' + arNum(it.n), W / 2, 760, { size: 90, align: 'center', color: C.ink, lang: 'ar', weight: 700, alpha: clamp(a / 0.3) });
    }
  }
  function dishScene(ctx, t, it) {
    // a setting that suits the dish: the river for masgouf, a dawn sky for pacha, a plain print ground otherwise
    sky(ctx);
    if (false) { sun(ctx, 300, 260, 110); clouds(ctx, t); malwiya(ctx, 1550, 760, 0.8); palm(ctx, 1300, 780, 0.8, 66); waves(ctx, 790, t, { color: C.sky, amp: 14, len: 260, speed: 25, foam: false, seed: 6 }); }
    else if (false) { const g = ctx.createLinearGradient(0, 300, 0, 800); g.addColorStop(0, 'rgba(231,184,160,0)'); g.addColorStop(1, C.pink); ctx.fillStyle = g; ctx.fillRect(0, 300, W, 500); sun(ctx, 260, 640, 90); clouds(ctx, t); }
    else { sun(ctx, 230 + it.n * 40, 230, 90); clouds(ctx, t); }
    // the table: a low wooden board
    rr(ctx, -20, 820, W + 40, 300, 0, C.brown, 950, 4);
    if (true) { ctx.save(); ctx.strokeStyle = 'rgba(28,26,23,0.35)'; ctx.lineWidth = 3; for (let k = 0; k < 6; k++) { ctx.beginPath(); ctx.moveTo(0, 860 + k * 40); ctx.lineTo(W, 850 + k * 42); ctx.stroke(); } ctx.restore(); }
    
    const bob = Math.sin(t * 1.3) * 4;
    printed(ctx, it.at, t, 0, W - 560, () => { ctx.save(); ctx.translate(720, 640 + bob); ctx.scale(1.25, 1.25); FOOD[it.n](ctx, t); ctx.restore(); });
    cartouche(ctx, it, t);
  }
  function outro(ctx, t) {
    landscape(ctx, t, { sunX: 400, sunY: 320 });
    const a = t - S.ev.outroAt, k = ease.outBack(clamp(a / 0.5), 1.6);
    ctx.save(); ctx.translate(W / 2 + 200, 380); ctx.scale(k, k);
    rr(ctx, -520, -170, 1040, 320, 8, C.ink, 820, 0); rr(ctx, -508, -158, 1016, 296, 6, C.cream, 821, 3);
    G.text(ctx, 'شنو لعبتك المفضلة؟', 0, -30, { size: 100, align: 'center', color: C.ink, lang: 'ar', weight: 700 });
    G.text(ctx, 'اكتبها بالتعليقات 👇', 0, 80, { size: 60, align: 'center', color: C.red, lang: 'ar' });
    ctx.restore();
    const s2 = ease.outBack(clamp((a - 4) / 0.4), 2);
    if (s2 > 0) { ctx.save(); ctx.translate(W / 2 + 200, 680); ctx.scale(s2, s2); rr(ctx, -230, -55, 460, 110, 55, C.red, 830); G.text(ctx, 'اشترك ⛩', 0, 22, { size: 64, align: 'center', color: C.cream, lang: 'ar', weight: 700 }); ctx.restore(); }
  }

  // ---------- the cut list ----------
  const shots = [{ t0: 0, draw: titleCard }, { t0: vo[0].at + 0.4, draw: intro }];
  for (const it of items) { shots.push({ t0: it.stamp, draw: (c, t) => stampScene(c, t, it) }); shots.push({ t0: it.at, draw: (c, t) => dishScene(c, t, it) }); }
  shots.push({ t0: S.ev.outroAt - 0.6, draw: outro });
  Studio.film({
    post: { paper: 0.6, vignette: 0.25, grain: 0.04 },
    fadeOut: 1.5,
    draw(ctx, t) {
      let i = 0; while (i + 1 < shots.length && t >= shots[i + 1].t0) i++;
      const sh = shots[i], local = t - sh.t0;
      // a slow push-in inside each shot
      const z = 1 + 0.03 * clamp(local / 15);
      ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
      sh.draw(ctx, t);
      ctx.restore();
      // a quick paper flash on each cut
      const f = 1 - clamp(local / 0.18);
      if (i > 0 && f > 0) { ctx.fillStyle = `rgba(235,221,188,${0.8 * f})`; ctx.fillRect(0, 0, W, H); }
    },
  });
})();
