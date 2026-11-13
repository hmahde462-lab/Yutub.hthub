// ArenaSim: one ball, many weapons, many containers. Deterministic (seeded), no glow.
// container: {sides: 0 (circle) | 3..8, R, rot, spin}
// cutters: axe | sword | dsword | laser | saw | shuriken | fan   (all split balls on contact)
// wallSplit: walls split the ball instead of a weapon.
(function (root) {
  function mulberry32(a) { return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const TAU = Math.PI * 2;
  function segDist(px, py, ax, ay, bx, by) { const vx = bx - ax, vy = by - ay, wx = px - ax, wy = py - ay, L = vx * vx + vy * vy; let u = L ? (wx * vx + wy * vy) / L : 0; u = Math.max(0, Math.min(1, u)); const cx = ax + vx * u, cy = ay + vy * u; return { d: Math.hypot(px - cx, py - cy), cx, cy, ux: vx, uy: vy }; }
  function collideBalls(bs, rest = 0.95) {
    for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++) {
      const a = bs[i], b = bs[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy, min = a.r + b.r;
      if (d2 >= min * min || d2 < 1e-9) continue;
      const d = Math.sqrt(d2), nx = dx / d, ny = dy / d, ma = a.r * a.r, mb = b.r * b.r, over = min - d;
      a.x -= nx * over * mb / (ma + mb); a.y -= ny * over * mb / (ma + mb); b.x += nx * over * ma / (ma + mb); b.y += ny * over * ma / (ma + mb);
      const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
      if (rv < 0) { const j2 = -(1 + rest) * rv / (1 / ma + 1 / mb); a.vx -= j2 * nx / ma; a.vy -= j2 * ny / ma; b.vx += j2 * nx / mb; b.vy += j2 * ny / mb; }
    }
  }
  class ArenaSim {
    constructor(cfg) {
      this.cfg = Object.assign({ seed: 1, fps: 60, sub: 8, cx: 540, cy: 930, g: 900, r0: 110, rMin: 10, floor: 850, maxTime: 30, wallSplit: false,
        container: { sides: 0, R: 420, rot: 0, spin: 0 }, cutters: [] }, cfg);
      const c = this.cfg; this.rng = mulberry32(c.seed); this.t = 0; this.frame = 0; this.events = []; this.state = 'run'; this.finaleT = null; this.shards = [];
      this.rot = c.container.rot || 0;
      this.cut = c.cutters.map((k, i) => Object.assign({ ang: (k.phase ?? 0), x: c.cx + (k.x ?? 0), y: c.cy + (k.y ?? 0), vx: k.vx ?? 0, vy: k.vy ?? 0, self: 0 }, k));
      const a = this.rng() * TAU; this.balls = [{ x: c.cx + (c.startX ?? -150), y: c.cy + (c.startY ?? -140), vx: Math.cos(a) * 380, vy: Math.sin(a) * 200, r: c.r0, gen: 0, cd: 0 }];
    }
    ev(kind, v, a) { this.events.push({ t: +this.t.toFixed(4), kind, v: +(+v).toFixed(3), a: +(+(a || 0)).toFixed(3) }); }
    get count() { return this.balls.length; }
    // ---- container geometry ----
    edges() { const C = this.cfg.container, n = C.sides; if (!n) return null; const out = [], ap = C.R * Math.cos(Math.PI / n);
      for (let k = 0; k < n; k++) { const a = this.rot + (k + .5) * TAU / n; out.push({ nx: Math.cos(a), ny: Math.sin(a), ap }); } return out; }
    verts() { const C = this.cfg.container, n = C.sides || 64, out = []; for (let k = 0; k < n; k++) { const a = this.rot + k * TAU / n; out.push([this.cfg.cx + Math.cos(a) * C.R, this.cfg.cy + Math.sin(a) * C.R]); } return out; }
    wall(b, cb) { const c = this.cfg, C = c.container, dx = b.x - c.cx, dy = b.y - c.cy; let hit = false;
      const reflect = (nx, ny, pen) => { b.x -= nx * pen; b.y -= ny * pen; const om = C.spin || 0, wvx = -om * (b.y - c.cy), wvy = om * (b.x - c.cx);
        const rvx = b.vx - wvx, rvy = b.vy - wvy, vn = rvx * nx + rvy * ny;
        if (vn > 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; const sp = Math.hypot(b.vx, b.vy); if (sp < c.floor) { b.vx *= c.floor / sp; b.vy *= c.floor / sp; } hit = true; cb && cb(Math.atan2(ny, nx), Math.min(1, vn / 1200), nx, ny); } };
      if (!C.sides) { const d = Math.hypot(dx, dy) || 1e-6, lim = C.R - b.r; if (d > lim) reflect(dx / d, dy / d, d - lim); }
      else for (const e of this.edges()) { const p = dx * e.nx + dy * e.ny, lim = e.ap - b.r; if (p > lim) reflect(e.nx, e.ny, p - lim); }
      return hit; }
    // ---- weapon geometry: list of {kind:'seg'|'disc', ..., cut:bool} ----
    parts(k) { const c = this.cfg, ca = Math.cos(k.ang), sa = Math.sin(k.ang), cx = c.cx, cy = c.cy, out = [];
      if (k.kind === 'axe') { const L = k.len ?? 330, hx = cx + ca * L, hy = cy + sa * L, bh = k.blade ?? 78;
        out.push({ kind: 'seg', a: [cx, cy], b: [hx, hy], w: 7, cut: false }); out.push({ kind: 'seg', a: [hx - sa * bh, hy + ca * bh], b: [hx + sa * bh, hy - ca * bh], w: 6, cut: true }); }
      else if (k.kind === 'sword' || k.kind === 'dsword') { const L = k.len ?? 360, h = k.hilt ?? 70;
        for (const sd of k.kind === 'dsword' ? [1, -1] : [1]) { out.push({ kind: 'seg', a: [cx, cy], b: [cx + ca * h * sd, cy + sa * h * sd], w: 9, cut: false }); out.push({ kind: 'seg', a: [cx + ca * h * sd, cy + sa * h * sd], b: [cx + ca * L * sd, cy + sa * L * sd], w: 7, cut: true }); } }
      else if (k.kind === 'laser') { const L = k.len ?? 440; out.push({ kind: 'seg', a: [cx - ca * L, cy - sa * L], b: [cx + ca * L, cy + sa * L], w: 4, cut: true }); }
      else if (k.kind === 'fan') { const L = k.len ?? 300, n = k.blades ?? 4; for (let i = 0; i < n; i++) { const a = k.ang + i * TAU / n; out.push({ kind: 'seg', a: [cx + Math.cos(a) * 40, cy + Math.sin(a) * 40], b: [cx + Math.cos(a) * L, cy + Math.sin(a) * L], w: 8, cut: true }); } }
      else if (k.kind === 'saw') { const o = k.orbit ?? 200; out.push({ kind: 'disc', x: cx + ca * o, y: cy + sa * o, rad: k.rad ?? 62, cut: true }); }
      else if (k.kind === 'shuriken') { out.push({ kind: 'disc', x: k.x, y: k.y, rad: k.rad ?? 46, cut: true }); }
      return out; }
    stepFrame() { const c = this.cfg, dt = 1 / c.fps / c.sub; for (let s = 0; s < c.sub; s++) this.substep(dt); this.frame++;
      if (this.state === 'run') { const allMin = this.balls.every(b => b.r / Math.SQRT2 < c.rMin); if ((allMin && this.count > 1) || this.t >= c.maxTime - 3.5) this.startFinale(); } }
    split(b, tx, ty, born, dead, bump) { const c = this.cfg, nr = b.r / Math.SQRT2; if (nr < c.rMin) return false;
      dead.add(b); const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
      for (const sd of [-1, 1]) born.push({ x: b.x + tx * sd * nr * .9, y: b.y + ty * sd * nr * .9, vx: b.vx * .6 + tx * sd * 420 + (bump ? bump[0] : 0), vy: b.vy * .6 + ty * sd * 420 + (bump ? bump[1] : 0), r: nr, gen: b.gen + 1, cd: .35 });
      this.ev('split', 1 - nr / c.r0, 0); return true; }
    substep(dt) {
      const c = this.cfg, C = c.container; this.t += dt;
      if (this.state === 'run') { this.rot += (C.spin || 0) * dt;
        for (const k of this.cut) { k.ang += (k.spin ?? 0) * dt; k.self += (k.selfSpin ?? 14) * dt;
          if (k.kind === 'shuriken') { k.x += k.vx * dt; k.y += k.vy * dt; const tmp = { x: k.x, y: k.y, vx: k.vx, vy: k.vy, r: k.rad ?? 46 }; const sv = c.floor; c.floor = 0; this.wall(tmp); c.floor = sv; k.x = tmp.x; k.y = tmp.y; k.vx = tmp.vx; k.vy = tmp.vy;
            const sp = Math.hypot(k.vx, k.vy) || 1, want = k.speed ?? 520; k.vx *= want / sp; k.vy *= want / sp; } } }
      for (const b of this.balls) { b.vy += c.g * dt; b.x += b.vx * dt; b.y += b.vy * dt; b.cd = Math.max(0, b.cd - dt); }
      collideBalls(this.balls);
      if (this.state !== 'run') { this.balls = this.balls.filter(b => b.y < 2150 && b.x > -100 && b.x < 1180);
        for (const s of this.shards) { s.vy += c.g * dt * .6; s.x += s.vx * dt; s.y += s.vy * dt; s.rot += s.vr * dt; } return; }
      const born = [], dead = new Set(), P = this.cut.map(k => this.parts(k));
      for (const b of this.balls) {
        const hitWall = this.wall(b, (a, v, nx, ny) => { this.ev('wall', v, a); if (c.wallSplit && b.cd === 0 && v > .25 && !dead.has(b)) this.split(b, -ny, nx, born, dead, [-nx * 260, -ny * 260]); });
        if (dead.has(b)) continue;
        for (const parts of P) { if (dead.has(b)) break;
          for (const p of parts) { if (dead.has(b)) break;
            if (p.kind === 'seg') { const s = segDist(b.x, b.y, p.a[0], p.a[1], p.b[0], p.b[1]); if (s.d >= b.r + p.w) continue;
              const nx = (b.x - s.cx) / (s.d || 1), ny = (b.y - s.cy) / (s.d || 1);
              if (p.cut && b.cd === 0 && this.split(b, s.ux, s.uy, born, dead, [nx * 160, ny * 160])) break;
              const vn = b.vx * nx + b.vy * ny; b.x = s.cx + nx * (b.r + p.w); b.y = s.cy + ny * (b.r + p.w); if (vn < 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; } if (p.cut) { b.cd = Math.max(b.cd, .08); this.ev('tink', .5, 0); } }
            else { const dx = b.x - p.x, dy = b.y - p.y, d = Math.hypot(dx, dy) || 1; if (d >= b.r + p.rad) continue; const nx = dx / d, ny = dy / d;
              if (p.cut && b.cd === 0 && this.split(b, -ny, nx, born, dead, [nx * 260, ny * 260])) break;
              const vn = b.vx * nx + b.vy * ny; b.x = p.x + nx * (b.r + p.rad); b.y = p.y + ny * (b.r + p.rad); if (vn < 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; } b.cd = Math.max(b.cd, .08); this.ev('tink', .5, 0); } } }
      }
      if (dead.size) this.balls = this.balls.filter(b => !dead.has(b)).concat(born);
    }
    startFinale() { const c = this.cfg; this.state = 'finale'; this.finaleT = this.t; this.finalCount = this.count; this.ev('boom', 1, 0);
      const V = this.verts(), n = V.length;
      for (let i = 0; i < n; i++) { const [x1, y1] = V[i], [x2, y2] = V[(i + 1) % n], segs = c.container.sides ? 6 : 1;
        for (let s = 0; s < segs; s++) { const u0 = s / segs, u1 = (s + 1) / segs, ax = x1 + (x2 - x1) * u0, ay = y1 + (y2 - y1) * u0, bx = x1 + (x2 - x1) * u1, by = y1 + (y2 - y1) * u1, mx = (ax + bx) / 2, my = (ay + by) / 2;
          const dx = mx - c.cx, dy = my - c.cy, d = Math.hypot(dx, dy) || 1, sp = 300 + this.rng() * 400;
          this.shards.push({ x: mx, y: my, len: Math.hypot(bx - ax, by - ay) * .95, vx: dx / d * sp, vy: dy / d * sp - 200, rot: Math.atan2(by - ay, bx - ax), vr: (this.rng() - .5) * 8 }); } }
      for (const b of this.balls) { const dx = b.x - c.cx, dy = b.y - c.cy, d = Math.hypot(dx, dy) || 1, sp = 500 + this.rng() * 600; b.vx += dx / d * sp; b.vy += dy / d * sp - 300; } }
  }
  root.ArenaSim = ArenaSim;
  if (typeof module !== 'undefined') module.exports = { ArenaSim };
})(typeof window !== 'undefined' ? window : globalThis);
