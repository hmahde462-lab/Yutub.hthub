// Two new mechanics, no glow: AxeSim (spinning axe splits balls) and GrowSim (two balls race to grow).
(function (root) {
  function mulberry32(a) { return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const TAU = Math.PI * 2;
  function segDist(px, py, ax, ay, bx, by) { const vx = bx - ax, vy = by - ay, wx = px - ax, wy = py - ay, L = vx * vx + vy * vy; let u = L ? (wx * vx + wy * vy) / L : 0; u = Math.max(0, Math.min(1, u)); const cx = ax + vx * u, cy = ay + vy * u; return { d: Math.hypot(px - cx, py - cy), cx, cy }; }
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
  function wall(b, c, floor, ev) {
    const dx = b.x - c.cx, dy = b.y - c.cy, d = Math.hypot(dx, dy) || 1e-6, lim = c.R - b.r;
    if (d <= lim) return false;
    const nx = dx / d, ny = dy / d, vn = b.vx * nx + b.vy * ny; b.x = c.cx + nx * lim; b.y = c.cy + ny * lim;
    if (vn > 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; const sp = Math.hypot(b.vx, b.vy); if (sp < floor) { b.vx *= floor / sp; b.vy *= floor / sp; } ev && ev(Math.atan2(dy, dx), Math.min(1, vn / 1200)); return true; }
    return false;
  }

  class AxeSim {
    constructor(cfg) {
      this.cfg = Object.assign({ seed: 3, fps: 60, sub: 8, cx: 540, cy: 930, R: 420, g: 900, r0: 112, rMin: 12, axeLen: 330, bladeHalf: 78, spin: 2.3, floor: 900, maxTime: 26 }, cfg);
      const c = this.cfg; this.rng = mulberry32(c.seed); this.t = 0; this.frame = 0; this.events = []; this.state = 'run'; this.finaleT = null; this.shards = [];
      this.nAxes = c.axes || 1; this.angs = Array.from({ length: this.nAxes }, (_, i) => -Math.PI / 2 + i * TAU / this.nAxes); this.spins = Array.from({ length: this.nAxes }, (_, i) => i === 0 ? c.spin : (i % 2 ? -1 : 1) * c.spin * (1 + .13 * i)); this.balls = [{ x: c.cx - 160, y: c.cy - 120, vx: 380, vy: 0, r: c.r0, gen: 0, cd: 0 }];
    }
    ev(kind, v, a) { this.events.push({ t: +this.t.toFixed(4), kind, v: +(+v).toFixed(3), a: +(+(a || 0)).toFixed(3) }); }
    get count() { return this.balls.length; }
    get ang() { return this.angs[0]; }
    axe(i = 0) { const c = this.cfg, ca = Math.cos(this.angs[i]), sa = Math.sin(this.angs[i]), hx = c.cx + ca * c.axeLen, hy = c.cy + sa * c.axeLen;
      return { hx, hy, ca, sa, b1: [hx - sa * c.bladeHalf, hy + ca * c.bladeHalf], b2: [hx + sa * c.bladeHalf, hy - ca * c.bladeHalf] }; }
    stepFrame() { const c = this.cfg, dt = 1 / c.fps / c.sub; for (let s = 0; s < c.sub; s++) this.substep(dt); this.frame++;
      if (this.state === 'run') { const allMin = this.balls.every(b => b.r / Math.SQRT2 < c.rMin); if ((allMin && this.count > 1) || this.t >= c.maxTime - 3.5) this.startFinale(); } }
    substep(dt) {
      const c = this.cfg; this.t += dt; if (this.state === 'run') for (let i = 0; i < this.nAxes; i++) this.angs[i] += this.spins[i] * dt;
      for (const b of this.balls) { b.vy += c.g * dt; b.x += b.vx * dt; b.y += b.vy * dt; b.cd = Math.max(0, b.cd - dt); }
      collideBalls(this.balls);
      if (this.state === 'run') {
        const born = [], dead = new Set();
        for (const b of this.balls) { if (dead.has(b)) continue;
          wall(b, c, c.floor, (a, v) => this.ev('wall', v, a));
          for (let ai = 0; ai < this.nAxes; ai++) { if (dead.has(b)) break; const A = this.axe(ai);
          // handle: bounce only
          const h = segDist(b.x, b.y, c.cx, c.cy, A.hx, A.hy);
          if (h.d < b.r + 7) { const nx = (b.x - h.cx) / (h.d || 1), ny = (b.y - h.cy) / (h.d || 1), vn = b.vx * nx + b.vy * ny; b.x = h.cx + nx * (b.r + 7); b.y = h.cy + ny * (b.r + 7); if (vn < 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; } }
          // blade: split
          const s = segDist(b.x, b.y, A.b1[0], A.b1[1], A.b2[0], A.b2[1]);
          if (s.d < b.r + 6 && b.cd === 0) {
            const nr = b.r / Math.SQRT2;
            if (nr >= c.rMin) {
              dead.add(b); const tx = -A.sa, ty = A.ca; // along the blade = across the cut
              for (const sd of [-1, 1]) born.push({ x: b.x + tx * sd * nr * .9 + A.ca * 4, y: b.y + ty * sd * nr * .9 + A.sa * 4, vx: b.vx * .6 + tx * sd * 420 + A.ca * 200, vy: b.vy * .6 + ty * sd * 420 + A.sa * 200, r: nr, gen: b.gen + 1, cd: .35 });
              this.ev('split', 1 - nr / c.r0, ai);
            } else { const nx = (b.x - s.cx) / (s.d || 1), ny = (b.y - s.cy) / (s.d || 1), vn = b.vx * nx + b.vy * ny; b.x = s.cx + nx * (b.r + 6); b.y = s.cy + ny * (b.r + 6); if (vn < 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; } b.cd = .1; this.ev('tink', .5, 0); }
          }
          }
        }
        if (dead.size) this.balls = this.balls.filter(b => !dead.has(b)).concat(born);
      } else { this.balls = this.balls.filter(b => b.y < 2100 && b.x > -80 && b.x < 1160); }
      for (const s of this.shards) { s.vy += c.g * dt * .6; s.x += s.vx * dt; s.y += s.vy * dt; s.rot += s.vr * dt; }
    }
    startFinale() { const c = this.cfg; this.state = 'finale'; this.finaleT = this.t; this.finalCount = this.count; this.ev('boom', 1, 0);
      for (let i = 0; i < 40; i++) { const a = i / 40 * TAU, sp = 300 + this.rng() * 400; this.shards.push({ x: c.cx + Math.cos(a) * c.R, y: c.cy + Math.sin(a) * c.R, len: TAU / 40 * c.R * .9, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 200, rot: a + Math.PI / 2, vr: (this.rng() - .5) * 8 }); }
      for (const b of this.balls) { const dx = b.x - c.cx, dy = b.y - c.cy, d = Math.hypot(dx, dy) || 1, sp = 500 + this.rng() * 600; b.vx += dx / d * sp; b.vy += dy / d * sp - 300; } }
  }

  class GrowSim {
    constructor(cfg) {
      this.cfg = Object.assign({ seed: 1, fps: 60, sub: 8, cx: 540, cy: 930, R: 420, g: 1100, r0: 34, grow: 1.055, winFrac: .6, floor: 950, maxTime: 30 }, cfg);
      const c = this.cfg; this.rng = mulberry32(c.seed); this.t = 0; this.frame = 0; this.events = []; this.state = 'run'; this.finaleT = null; this.winner = null; this.leadChanges = 0; this.lead = -1;
      const a1 = this.rng() * TAU, a2 = this.rng() * TAU;
      this.balls = [{ x: c.cx - 150, y: c.cy - 100, vx: Math.cos(a1) * 700, vy: Math.sin(a1) * 700, r: c.r0, team: 0, pop: 0 }, { x: c.cx + 150, y: c.cy - 100, vx: Math.cos(a2) * 700, vy: Math.sin(a2) * 700, r: c.r0, team: 1, pop: 0 }];
      this.particles = [];
    }
    ev(kind, v, team) { this.events.push({ t: +this.t.toFixed(4), kind, v: +(+v).toFixed(3), team: team ?? -1 }); }
    stepFrame() { const c = this.cfg, dt = 1 / c.fps / c.sub; for (let s = 0; s < c.sub; s++) this.substep(dt); this.frame++;
      if (this.state === 'run') { const [a, b] = this.balls, l = a.r > b.r + .5 ? 0 : (b.r > a.r + .5 ? 1 : this.lead); if (l !== this.lead && l >= 0) { if (this.lead >= 0) this.leadChanges++; this.lead = l; }
        const w = this.balls.find(x => x.r >= c.R * c.winFrac); if (w || this.t >= c.maxTime - 3.5) { this.winner = w ? w.team : (a.r >= b.r ? 0 : 1); this.startFinale(); } } }
    substep(dt) {
      const c = this.cfg; this.t += dt;
      for (const b of this.balls) { b.vy += c.g * dt; b.x += b.vx * dt; b.y += b.vy * dt; b.pop = Math.max(0, b.pop - dt * 4);
        if (this.state === 'run' || b.team === this.winner) { if (wall(b, c, c.floor, (a, v) => { if (this.state === 'run') { const lim = c.R * c.winFrac * 1.02; b.r = Math.min(lim, b.r * c.grow); b.pop = 1; this.ev('grow', b.r / (c.R * c.winFrac), b.team); } })) {} } }
      collideBalls(this.balls, 1.0);
      this.balls = this.balls.filter(b => b.y < 2300);
      for (const p of this.particles) { p.vy += 900 * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt; }
      this.particles = this.particles.filter(p => p.life > 0);
    }
    startFinale() { const c = this.cfg; this.state = 'finale'; this.finaleT = this.t; this.ev('win', 1, this.winner);
      const loser = this.balls.find(b => b.team !== this.winner);
      if (loser) { for (let i = 0; i < 46; i++) { const a = this.rng() * TAU, sp = 200 + this.rng() * 700; this.particles.push({ x: loser.x, y: loser.y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 300, life: 2 + this.rng(), team: loser.team, r: 6 + this.rng() * 10 }); }
        this.balls = this.balls.filter(b => b !== loser); this.ev('pop', 1, loser.team); } }
  }
  root.AxeSim = AxeSim; root.GrowSim = GrowSim;
  if (typeof module !== 'undefined') module.exports = { AxeSim, GrowSim };
})(typeof window !== 'undefined' ? window : globalThis);
