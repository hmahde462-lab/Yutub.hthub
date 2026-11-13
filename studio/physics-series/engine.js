// Deterministic 2D ball physics for the "satisfying" series.
// Pure logic, no drawing: runs in Node (for tuning) and in the browser (for rendering).
(function (root) {
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const TAU = Math.PI * 2;
  const wrap = (a) => { a = (a + Math.PI) % TAU; if (a < 0) a += TAU; return a - Math.PI; };

  class Sim {
    constructor(cfg) {
      this.cfg = Object.assign({
        seed: 7, fps: 60, sub: 8, cx: 540, cy: 930, R: 420, ringWidth: 8,
        gapDeg: 44, ringSpeed: 1.1, g: 650, ballR: 13, restBall: 0.92,
        spawnPer: 2, spawnSpeed: [700, 1000], minBounce: 950, cap: 450, maxTime: 26, finaleAt: null,
        palette: ['#ffe14d', '#b14dff', '#3dff8a', '#ff4d4d', '#3d7bff', '#ff9a3d', '#3df2ff', '#ff4dc4'],
      }, cfg);
      const c = this.cfg;
      this.rng = mulberry32(c.seed);
      this.t = 0; this.frame = 0; this.ringAngle = -Math.PI / 2; this.balls = []; this.outBalls = [];
      this.events = []; this.escapes = 0; this.state = 'run'; this.shards = []; this.finaleT = null;
      this.gapHalf = (c.gapDeg / 2) * Math.PI / 180;
      this.add(c.cx, c.cy - 120, 260, -80, 0);
    }
    add(x, y, vx, vy, gen) { this.balls.push({ x, y, vx, vy, r: this.cfg.ballR, gen }); }
    ev(kind, v, a) { this.events.push({ t: +this.t.toFixed(4), kind, v: +v.toFixed(3), a: a === undefined ? 0 : +a.toFixed(3) }); }
    get count() { return this.balls.length; }

    stepFrame() {
      const c = this.cfg, dt = 1 / c.fps / c.sub;
      for (let s = 0; s < c.sub; s++) this.substep(dt);
      this.frame++;
      if (this.state === 'run') {
        const capHit = this.count >= c.cap;
        const timeUp = this.t >= (c.finaleAt ?? c.maxTime - 3.2);
        if (capHit || timeUp) this.startFinale();
      }
    }

    substep(dt) {
      const c = this.cfg; this.t += dt;
      if (this.state === 'run') this.ringAngle = wrap(this.ringAngle + c.ringSpeed * dt);
      const balls = this.balls;
      for (const b of balls) { b.vy += c.g * dt; b.x += b.vx * dt; b.y += b.vy * dt; }
      this.collideBalls();
      if (this.state === 'run') {
        const keep = [];
        for (const b of balls) { if (!this.ringCollide(b)) keep.push(b); }
        if (keep.length !== balls.length) this.balls = keep;
      }
      for (const o of this.outBalls) { o.vy += c.g * dt; o.x += o.vx * dt; o.y += o.vy * dt; o.life -= dt; }
      this.outBalls = this.outBalls.filter((o) => o.y < 2100 && o.life > 0);
      for (const s of this.shards) { s.vy += c.g * dt * 0.6; s.x += s.vx * dt; s.y += s.vy * dt; s.rot += s.vr * dt; s.life -= dt; }
      if (this.state === 'finale') this.balls = this.balls.filter((b) => b.y < 2100 && b.x > -60 && b.x < 1140);
    }

    // returns true if the ball escaped (and was removed)
    ringCollide(b) {
      const c = this.cfg, dx = b.x - c.cx, dy = b.y - c.cy, d = Math.hypot(dx, dy) || 1e-6;
      const ang = Math.atan2(dy, dx), rel = wrap(ang - this.ringAngle);
      const inGap = Math.abs(rel) < this.gapHalf - (b.r / c.R) * 0.6;
      if (inGap && d - b.r > c.R + c.ringWidth) { this.escape(b, ang); return true; }
      if (!inGap && d + b.r > c.R - c.ringWidth / 2 && d < c.R + c.ringWidth) {
        const nx = dx / d, ny = dy / d, vn = b.vx * nx + b.vy * ny;
        if (vn > 0) {
          b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny;
          // keep the show lively: a floor on bounce speed
          const sp = Math.hypot(b.vx, b.vy); const fl = c.minBounce; if (sp < fl) { b.vx *= fl / sp; b.vy *= fl / sp; }
          this.ev('ring', Math.min(1, vn / 900), ang);
        }
        const target = c.R - c.ringWidth / 2 - b.r; b.x = c.cx + nx * target; b.y = c.cy + ny * target;
      }
      // gap edges behave like round posts
      for (const sgn of [-1, 1]) {
        const ea = this.ringAngle + sgn * this.gapHalf, px = c.cx + Math.cos(ea) * c.R, py = c.cy + Math.sin(ea) * c.R;
        const ex = b.x - px, ey = b.y - py, ed = Math.hypot(ex, ey), min = b.r + c.ringWidth / 2;
        if (ed < min && ed > 1e-6) {
          const nx = ex / ed, ny = ey / ed, vn = b.vx * nx + b.vy * ny;
          b.x = px + nx * min; b.y = py + ny * min;
          if (vn < 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; this.ev('post', Math.min(1, -vn / 900), ea); }
        }
      }
      return false;
    }

    escape(b, ang) {
      const c = this.cfg; this.escapes++;
      this.outBalls.push({ x: b.x, y: b.y, vx: b.vx, vy: b.vy, r: b.r, gen: b.gen, life: 2.5 });
      this.ev('escape', 1, ang);
      if (this.count - 1 + c.spawnPer > c.cap) return;
      for (let i = 0; i < c.spawnPer; i++) {
        const a = this.rng() * TAU, sp = c.spawnSpeed[0] + this.rng() * (c.spawnSpeed[1] - c.spawnSpeed[0]);
        const j = (this.rng() - 0.5) * 30;
        this.add(c.cx + j, c.cy + j, Math.cos(a) * sp, Math.sin(a) * sp, b.gen + 1);
      }
      this.ev('spawn', 1, 0);
    }

    collideBalls() {
      const balls = this.balls, n = balls.length; if (n < 2) return;
      const cell = this.cfg.ballR * 2.2, grid = new Map();
      for (let i = 0; i < n; i++) {
        const b = balls[i], k = ((b.x / cell) | 0) * 4096 + ((b.y / cell) | 0);
        let arr = grid.get(k); if (!arr) { arr = []; grid.set(k, arr); } arr.push(i);
      }
      const e = this.cfg.restBall;
      for (let i = 0; i < n; i++) {
        const a = balls[i], gx = (a.x / cell) | 0, gy = (a.y / cell) | 0;
        for (let ox = -1; ox <= 1; ox++) for (let oy = -1; oy <= 1; oy++) {
          const arr = grid.get((gx + ox) * 4096 + (gy + oy)); if (!arr) continue;
          for (const j of arr) {
            if (j <= i) continue;
            const b = balls[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy, min = a.r + b.r;
            if (d2 >= min * min || d2 < 1e-9) continue;
            const d = Math.sqrt(d2), nx = dx / d, ny = dy / d, over = (min - d) / 2;
            a.x -= nx * over; a.y -= ny * over; b.x += nx * over; b.y += ny * over;
            const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
            if (rv < 0) { const imp = -(1 + e) * rv / 2; a.vx -= imp * nx; a.vy -= imp * ny; b.vx += imp * nx; b.vy += imp * ny; }
          }
        }
      }
    }

    startFinale() {
      const c = this.cfg; this.state = 'finale'; this.finaleT = this.t; this.finalCount = this.count;
      this.ev('boom', 1, 0);
      const N = 48;
      for (let i = 0; i < N; i++) {
        const a0 = (i / N) * TAU, rel = wrap(a0 - this.ringAngle);
        if (Math.abs(rel) < this.gapHalf) continue;
        const sp = 250 + this.rng() * 450;
        this.shards.push({ x: c.cx + Math.cos(a0) * c.R, y: c.cy + Math.sin(a0) * c.R, a0, len: TAU / N * c.R * 0.9,
          vx: Math.cos(a0) * sp, vy: Math.sin(a0) * sp - 200, rot: a0 + Math.PI / 2, vr: (this.rng() - 0.5) * 8, life: 4 });
      }
      for (const b of this.balls) {
        const dx = b.x - c.cx, dy = b.y - c.cy, d = Math.hypot(dx, dy) || 1, sp = 500 + this.rng() * 700;
        b.vx += dx / d * sp; b.vy += dy / d * sp - 250;
      }
    }
  }
  root.PhysicsSim = Sim;
  if (typeof module !== 'undefined') module.exports = { Sim };
})(typeof window !== 'undefined' ? window : globalThis);
