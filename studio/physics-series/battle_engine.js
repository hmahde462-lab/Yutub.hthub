// "Colour battle": top-down arena, teams of balls convert each other on contact.
// Deterministic (seeded); runs in Node for seed tuning and in the browser for rendering.
(function (root) {
  function mulberry32(a) { return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const TAU = Math.PI * 2;
  class Battle {
    constructor(cfg) {
      this.cfg = Object.assign({ seed: 1, fps: 60, sub: 6, cx: 540, cy: 930, R: 400, ballR: 38, perTeam: 8,
        teams: 4, speed: 560, cooldown: 0.22, maxTime: 27, jitterDeg: 9 }, cfg);
      const c = this.cfg; this.rng = mulberry32(c.seed);
      this.t = 0; this.frame = 0; this.events = []; this.state = 'run'; this.finaleT = null; this.winner = null;
      this.balls = []; this.history = []; this.eliminated = [];
      // each team starts as a cluster in its own quadrant
      const quad = [[-1, -1], [1, -1], [-1, 1], [1, 1]];
      const inR = c.sides ? c.R * Math.cos(Math.PI / c.sides) : c.R;
      for (let tm = 0; tm < c.teams; tm++) {
        const baseA = c.teams === 4 && !c.sides ? Math.atan2(quad[tm][1], quad[tm][0]) : -Math.PI / 2 + tm * 2 * Math.PI / c.teams + Math.PI / c.teams;
        const spreadA = c.teams === 4 && !c.sides ? 1.3 : Math.min(1.6, 2 * Math.PI / c.teams * .8);
        let placed = 0, guard = 0;
        while (placed < c.perTeam && guard++ < 5000) {
          const ang = baseA + (this.rng() - 0.5) * spreadA;
          const rad = 70 + this.rng() * (inR - c.ballR - (c.sides ? 25 : 90));
          const x = c.cx + Math.cos(ang) * rad, y = c.cy + Math.sin(ang) * rad;
          if (this.balls.some(b => Math.hypot(b.x - x, b.y - y) < c.ballR * 2.15)) continue;
          const a = this.rng() * TAU;
          this.balls.push({ x, y, vx: Math.cos(a) * c.speed, vy: Math.sin(a) * c.speed, r: c.ballR, team: tm, cd: 0, spin: this.rng() * TAU, pop: 0 });
          placed++;
        }
      }
    }
    counts() { const n = new Array(this.cfg.teams).fill(0); for (const b of this.balls) n[b.team]++; return n; }
    ev(kind, v, team) { this.events.push({ t: +this.t.toFixed(4), kind, v: +(+v).toFixed(3), team: team ?? -1 }); }
    stepFrame() {
      const c = this.cfg, dt = 1 / c.fps / c.sub;
      for (let s = 0; s < c.sub; s++) this.substep(dt);
      this.frame++;
      if (this.frame % 6 === 0) this.history.push(this.counts());
      if (this.state === 'run') {
        const n = this.counts(), alive = n.filter(x => x > 0).length;
        n.forEach((x, tm) => { if (x === 0 && !this.eliminated.includes(tm)) { this.eliminated.push(tm); this.ev('elim', 1, tm); } });
        if (alive === 1 || this.t >= c.maxTime) {
          const max = Math.max(...n); this.winner = n.indexOf(max); this.startFinale();
        }
      }
    }
    substep(dt) {
      const c = this.cfg; this.t += dt;
      for (const b of this.balls) {
        b.x += b.vx * dt; b.y += b.vy * dt; b.cd = Math.max(0, b.cd - dt); b.pop = Math.max(0, b.pop - dt * 3);
        const sp = Math.hypot(b.vx, b.vy) || 1;
        { const k = 1 + 0.08 * (c.speed / sp - 1); b.vx *= k; b.vy *= k; }
        b.spin += (sp / b.r) * dt * (b.vx >= 0 ? 1 : -1) * 0.5;
        this.wall(b);
      }
      this.collide();
    }
    wall(b) {
      const c = this.cfg, dx = b.x - c.cx, dy = b.y - c.cy;
      let nx, ny, pen = 0;
      if (c.sides) { const ap = c.R * Math.cos(Math.PI / c.sides); for (let k = 0; k < c.sides; k++) { const a = (c.rot || 0) + (k + .5) * 2 * Math.PI / c.sides, ex = Math.cos(a), ey = Math.sin(a), p = dx * ex + dy * ey - (ap - b.r); if (p > pen) { pen = p; nx = ex; ny = ey; } } if (pen <= 0) return; b.x -= nx * pen; b.y -= ny * pen; }
      else { const d = Math.hypot(dx, dy) || 1e-6, lim = c.R - b.r; if (d <= lim) return; nx = dx / d; ny = dy / d; b.x = c.cx + nx * lim; b.y = c.cy + ny * lim; }
      const vn = b.vx * nx + b.vy * ny;
      if (vn > 0) {
        b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny;
        const j = (this.rng() - 0.5) * 2 * c.jitterDeg * Math.PI / 180, cs = Math.cos(j), sn = Math.sin(j);
        const vx = b.vx * cs - b.vy * sn; b.vy = b.vx * sn + b.vy * cs; b.vx = vx;
        this.ev('wall', Math.min(1, vn / c.speed), b.team);
      }
    }
    collide() {
      const bs = this.balls, n = bs.length;
      for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
        const a = bs[i], b = bs[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy, min = a.r + b.r;
        if (d2 >= min * min || d2 < 1e-9) continue;
        const d = Math.sqrt(d2), nx = dx / d, ny = dy / d, over = (min - d) / 2;
        a.x -= nx * over; a.y -= ny * over; b.x += nx * over; b.y += ny * over;
        const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny;
        if (rv < 0) {
          a.vx += rv * nx; a.vy += rv * ny; b.vx -= rv * nx; b.vy -= rv * ny;
          this.ev('hit', Math.min(1, -rv / (2 * this.cfg.speed)), -1);
          if (this.state === 'run' && a.team !== b.team && a.cd === 0 && b.cd === 0) {
            const [win, lose] = this.rng() < 0.5 ? [a, b] : [b, a];
            lose.team = win.team; lose.pop = 1; a.cd = b.cd = this.cfg.cooldown;
            this.ev('convert', 1, win.team);
          }
        }
      }
    }
    startFinale() {
      const c = this.cfg; this.state = 'finale'; this.finaleT = this.t; this.finalCounts = this.counts();
      this.ev('win', 1, this.winner);
      for (const b of this.balls) { if (b.team !== this.winner) { b.team = this.winner; b.pop = 1; } }
    }
  }
  root.Battle = Battle;
  if (typeof module !== 'undefined') module.exports = { Battle };
})(typeof window !== 'undefined' ? window : globalThis);
