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
    10(ctx, t) { // falafel wrap with amba
      plate(ctx, 0, 60);
      poly(ctx, [[-260, 40], [220, -60], [250, 30], [-230, 110]], C.ochre, 100);
      for (let i = 0; i < 6; i++) ell(ctx, -150 + i * 70, 10 - i * 18, 34, 30, C.brown, 110 + i);
      for (let i = 0; i < 3; i++) ell(ctx, -100 + i * 110, -24 - i * 20, 30, 12, C.red, 120 + i, 3);
      for (let i = 0; i < 5; i++) { const x = -170 + i * 85, y = 30 - i * 20, d = 16 + 10 * Math.sin(t * 2 + i); poly(ctx, [[x - 12, y], [x + 12, y], [x + 4, y + d + 20], [x - 4, y + d + 20]], '#E8B53A', 130 + i, 2.5); }
      ell(ctx, 260, 110, 50, 20, C.green, 140, 3);
    },
    9(ctx, t) { // tashreeb
      bowl(ctx, 0, 0, 300, 200, C.indigo, '#8A4B2A');
      for (let i = 0; i < 9; i++) poly(ctx, [[-220 + i * 50, -30 + (i % 3) * 14], [-180 + i * 50, -40 + (i % 2) * 10], [-170 + i * 50, -6], [-215 + i * 50, 0]], C.ochre, 150 + i, 3);
      for (let i = 0; i < 10; i++) ell(ctx, -200 + R(i, 4) * 400, -30 + R(i, 5) * 40, 10, 9, C.cream, 160 + i, 2);
      for (let i = 0; i < 3; i++) ell(ctx, -120 + i * 120, -12, 18, 18, '#2A2018', 170 + i, 3);
      steam(ctx, 0, -60, t, 3, 240, 175);
    },
    8(ctx, t) { // kleicha
      plate(ctx, 0, 60);
      const pos = [[-180, 30], [-60, 0], [60, 20], [180, 40], [-120, 90], [0, 80], [120, 100]];
      pos.forEach(([x, y], i) => {
        ell(ctx, x, y - 20, 62, 30, C.ochre, 180 + i);
        ctx.save(); ctx.strokeStyle = C.brown; ctx.lineWidth = 3;
        for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2; ctx.beginPath(); ctx.moveTo(x, y - 20); ctx.lineTo(x + Math.cos(a) * 44, y - 20 + Math.sin(a) * 20); ctx.stroke(); }
        ctx.restore();
        if (i % 3 === 0) ell(ctx, x, y - 20, 18, 9, C.dark, 190 + i, 2);
      });
    },
    7(ctx, t) { // kubba halab
      plate(ctx, 0, 60);
      const pos = [[-170, 20], [-50, -10], [70, 15], [190, 30], [-110, 70], [10, 70], [130, 85]];
      pos.forEach(([x, y], i) => { ctx.save(); ctx.translate(x, y - 20); ctx.rotate(-0.4); ell(ctx, 0, 0, 62, 34, '#D98A2B', 200 + i); ell(ctx, -14, -10, 22, 8, '#F0C070', 210 + i, 0); ctx.restore(); });
      // torshi on the side
      bowl(ctx, 330, -30, 90, 80, C.cream, C.purple);
      for (let i = 0; i < 4; i++) ell(ctx, 290 + i * 26, -34, 12, 8, i % 2 ? C.red : '#E8B53A', 220 + i, 2);
    },
    6(ctx, t) { // pacha: a big copper pot at dawn
      poly(ctx, [[-260, -60], [260, -60], [220, 150], [-220, 150]], '#B8692E', 230);
      ell(ctx, 0, -60, 260, 50, '#7A3B1A', 231);
      ell(ctx, 0, -60, 220, 36, '#C9A15A', 232, 3);
      for (let i = 0; i < 5; i++) ell(ctx, -150 + i * 75, -66 + (i % 2) * 8, 34, 16, C.pink, 233 + i, 3);
      rr(ctx, -300, -40, 40, 30, 10, C.dark, 240); rr(ctx, 260, -40, 40, 30, 10, C.dark, 241);
      steam(ctx, 0, -100, t, 4, 300, 245);
      // bread and lemon beside it
      poly(ctx, [[-430, 120], [-300, 80], [-280, 150], [-420, 170]], C.ochre, 250);
      ell(ctx, 330, 130, 40, 30, '#E8D23A', 251);
    },
    5(ctx, t) { // biryani
      plate(ctx, 0, 70, 380, 130);
      poly(ctx, [[-290, 60], [-200, -60], [-60, -130], [80, -130], [210, -60], [290, 60]], '#E8B53A', 260);
      for (let i = 0; i < 70; i++) { const x = -250 + R(i, 6) * 500, y = 40 - R(i, 7) * 150 * (1 - Math.abs(x) / 300); ln(ctx, [[x, y], [x + 10, y - 3]], C.cream, 3, 300 + i); }
      for (let i = 0; i < 8; i++) ell(ctx, -200 + R(i, 8) * 400, -10 - R(i, 9) * 70, 14, 7, C.cream, 270 + i, 2); // almonds
      for (let i = 0; i < 8; i++) ell(ctx, -200 + R(i, 10) * 400, -10 - R(i, 11) * 70, 7, 7, C.purple, 280 + i, 2); // raisins
      for (let i = 0; i < 5; i++) rr(ctx, -230 + i * 100, 50 - (i % 2) * 20, 40, 34, 6, '#C98B2E', 290 + i, 3); // potatoes
      ell(ctx, 40, -120, 80, 46, '#B0612A', 295); ell(ctx, 120, -150, 22, 22, C.cream, 296, 3); // chicken
      steam(ctx, 0, -170, t, 3, 200, 297);
    },
    4(ctx, t) { // tepsi: the oven tray
      poly(ctx, [[-360, -40], [360, -40], [400, 130], [-400, 130]], C.dark, 330);
      poly(ctx, [[-330, -24], [330, -24], [362, 110], [-362, 110]], '#9E3A24', 331, 3);
      for (let r = 0; r < 3; r++) for (let c = 0; c < 7; c++) {
        const x = -270 + c * 90 + (r % 2) * 40, y = 0 + r * 40, k = (r + c) % 3;
        ell(ctx, x, y, 40, 16, [C.purple, C.red, '#E0B860'][k], 340 + r * 10 + c, 3);
      }
      steam(ctx, 0, -40, t, 4, 220, 380);
    },
    3(ctx, t) { // quzi
      plate(ctx, 0, 90, 420, 140);
      poly(ctx, [[-330, 80], [-220, -40], [-60, -90], [100, -90], [240, -40], [330, 80]], '#E8C25A', 400);
      // the lamb, stylized and lying down, golden roasted
      ell(ctx, 0, -110, 210, 80, '#9B5428', 410);
      for (let k = 0; k < 5; k++) ln(ctx, [[-150 + k * 70, -170 + Math.abs(k - 2) * 10], [-130 + k * 70, -60]], '#6A3016', 4, 412 + k);
      ell(ctx, -60, -150, 50, 14, '#C27A3A', 418, 0);
      for (let i = 0; i < 14; i++) ell(ctx, -280 + R(i, 12) * 560, 40 - R(i, 13) * 40, 12, 6, C.cream, 420 + i, 2);
      for (let i = 0; i < 8; i++) ell(ctx, -280 + R(i, 14) * 560, 40 - R(i, 15) * 40, 8, 8, C.green, 440 + i, 2);
      steam(ctx, 0, -200, t, 3, 180, 450);
    },
    2(ctx, t) { // dolma, the turned-out pot
      plate(ctx, 0, 90, 400, 135);
      // a dome of rolls
      const rows = [[7, 50], [6, -10], [5, -65], [3, -115]];
      rows.forEach(([n, y], r) => { for (let i = 0; i < n; i++) { const x = (i - (n - 1) / 2) * 78, k = (i + r) % 4; const fill = [C.sage, C.cream, C.purple, C.red][k]; ell(ctx, x, y, 38, 30, fill, 460 + r * 10 + i); if (k === 1) { ctx.save(); ctx.strokeStyle = C.ochre; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, y, 24, 18, 0, 0, Math.PI * 2); ctx.stroke(); ctx.restore(); } if (k === 0) ln(ctx, [[x - 24, y - 6], [x + 24, y + 6]], C.green, 2, 470 + i); } });
      steam(ctx, 0, -150, t, 3, 200, 490);
    },
    1(ctx, t) { // masgouf: the split fish on stakes around a wood fire by the Tigris
      // fire
      for (let i = 0; i < 7; i++) { const x = -60 + i * 22, f = 40 * Math.sin(t * 7 + i * 1.3); poly(ctx, [[x - 26, 160], [x + 26, 160], [x + 8 + f * 0.2, 40 - f], [x - 4, 80]], i % 2 ? C.red : C.ochre, 500 + i, 3); }
      for (let i = 0; i < 4; i++) rr(ctx, -110 + i * 50, 150, 70, 22, 10, C.dark, 510 + i, 3);
      // stakes + the butterflied fish facing the fire
      for (const sx of [-1, 1]) {
        ctx.save(); ctx.translate(sx * 260, 0); ctx.scale(sx, 1);
        ln(ctx, [[0, 170], [-10, -200]], C.dark, 10, 520);
        poly(ctx, [[-130, -170], [40, -200], [120, -120], [130, 0], [60, 120], [-80, 140], [-150, 40]], '#D7653A', 521);
        poly(ctx, [[-100, -140], [30, -165], [90, -100], [96, 0], [40, 96], [-60, 110], [-110, 30]], '#F0A060', 522, 3);
        for (let k = 0; k < 6; k++) ln(ctx, [[-90 + k * 6, -120 + k * 40], [70 - k * 4, -110 + k * 38]], '#C04A28', 3, 523 + k);
        poly(ctx, [[-60, -190], [40, -200], [0, -260]], '#B44A2A', 529);
        ell(ctx, -6, -222, 10, 10, C.cream, 531, 3); ell(ctx, -6, -222, 4, 4, C.ink, 532, 0);
        poly(ctx, [[-20, 120], [-70, 210], [40, 200]], '#B44A2A', 530);
        ctx.restore();
      }
      steam(ctx, 0, 10, t, 3, 260, 540);
    },
  };

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
    G.text(ctx, 'أطيب ١٠ أكلات عراقية', 0, -20, { size: 120, align: 'center', color: C.ink, lang: 'ar', weight: 700 });
    G.text(ctx, 'TOP 10 IRAQI FOODS · UKIYO-E', 0, 70, { size: 40, align: 'center', color: C.prussian, fam: 'Bungee', weight: 400 });
    ctx.restore();
    seal(ctx, W / 2 + 470, 540, 0.75 * k, 10, 0.08);
  }
  function intro(ctx, t) { // the panorama while the intro is spoken
    landscape(ctx, t);
    const a = clamp((t - vo[0].at) / 1);
    G.text(ctx, 'من بغداد… بعيون يابانية', W / 2, 260, { size: 80, align: 'center', color: C.ink, lang: 'ar', weight: 700, alpha: a });
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
    if (it.n === 1) { sun(ctx, 300, 260, 110); clouds(ctx, t); malwiya(ctx, 1550, 760, 0.8); palm(ctx, 1300, 780, 0.8, 66); waves(ctx, 790, t, { color: C.sky, amp: 14, len: 260, speed: 25, foam: false, seed: 6 }); }
    else if (it.n === 6) { const g = ctx.createLinearGradient(0, 300, 0, 800); g.addColorStop(0, 'rgba(231,184,160,0)'); g.addColorStop(1, C.pink); ctx.fillStyle = g; ctx.fillRect(0, 300, W, 500); sun(ctx, 260, 640, 90); clouds(ctx, t); }
    else { sun(ctx, 230 + it.n * 40, 230, 90); clouds(ctx, t); }
    // the table: a low wooden board
    rr(ctx, -20, 820, W + 40, 300, 0, it.n === 1 ? C.prussian : C.brown, 950, 4);
    if (it.n !== 1) { ctx.save(); ctx.strokeStyle = 'rgba(28,26,23,0.35)'; ctx.lineWidth = 3; for (let k = 0; k < 6; k++) { ctx.beginPath(); ctx.moveTo(0, 860 + k * 40); ctx.lineTo(W, 850 + k * 42); ctx.stroke(); } ctx.restore(); }
    else waves(ctx, 900, t, { color: C.indigo, amp: 26, len: 260, speed: 50, seed: 7 });
    const bob = Math.sin(t * 1.3) * 4;
    printed(ctx, it.at, t, 0, W - 560, () => { ctx.save(); ctx.translate(720, 640 + bob); ctx.scale(1.25, 1.25); FOOD[it.n](ctx, t); ctx.restore(); });
    cartouche(ctx, it, t);
  }
  function outro(ctx, t) {
    landscape(ctx, t, { sunX: 400, sunY: 320 });
    const a = t - S.ev.outroAt, k = ease.outBack(clamp(a / 0.5), 1.6);
    ctx.save(); ctx.translate(W / 2 + 200, 380); ctx.scale(k, k);
    rr(ctx, -520, -170, 1040, 320, 8, C.ink, 820, 0); rr(ctx, -508, -158, 1016, 296, 6, C.cream, 821, 3);
    G.text(ctx, 'شنو أكلتك المفضلة؟', 0, -30, { size: 100, align: 'center', color: C.ink, lang: 'ar', weight: 700 });
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
