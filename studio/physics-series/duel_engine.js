// DuelSim: 2-4 named balls with 100 HP. Weapons/items spawn at random, a ball that touches one picks it up.
// Held weapons orbit (or point) and deal damage to other balls. Last ball standing wins. Seeded & deterministic.
(function (root) {
  function mulberry32(a) { return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const TAU = Math.PI * 2;
  // held weapons: reach from ball edge, spin rad/s, damage, per-target cooldown, knockback
  const WEAPONS = {
    sword:  { inner: 4, outer: 95, spin: 7.5, dmg: 14, cd: .45, kb: 520, uses: 6 },
    knife:  { inner: 4, outer: 52, spin: 11, dmg: 9, cd: .3, kb: 300, uses: 8 },
    axe:    { inner: 4, outer: 84, spin: 5.2, dmg: 20, cd: .6, kb: 700, uses: 5 },
    hammer: { inner: 4, outer: 80, spin: 4.6, dmg: 17, cd: .6, kb: 1100, uses: 5 },
    spear:  { inner: 4, outer: 130, spin: 0, dmg: 15, cd: .5, kb: 650, uses: 6, point: true },
    saw:    { orbit: 50, rad: 26, spin: 6, dmg: 7, cd: .22, kb: 260, uses: 12, disc: true },
  };
  const ITEMS = ['heal', 'shield', 'bomb', 'speed'];
  function segDist(px, py, ax, ay, bx, by) { const vx = bx - ax, vy = by - ay, wx = px - ax, wy = py - ay, L = vx * vx + vy * vy; let u = L ? (wx * vx + wy * vy) / L : 0; u = Math.max(0, Math.min(1, u)); const cx = ax + vx * u, cy = ay + vy * u; return Math.hypot(px - cx, py - cy); }
  class DuelSim {
    constructor(cfg) {
      this.cfg = Object.assign({ seed: 1, fps: 60, sub: 4, cx: 540, cy: 930, sides: 0, R: 430, rot: 0, shrinkFrom: null, shrinkTo: null, shrinkDur: 14,
        r: 54, speed: 430, hp: 100, spawnEvery: 2.0, firstSpawn: 1.2, itemLife: 5.5, holdTime: 7, bump: 2, dmgScale: 1, maxTime: 40,
        pool: ['sword', 'knife', 'axe', 'hammer', 'spear', 'saw', 'heal', 'shield', 'bomb'], fighters: [] }, cfg);
      const c = this.cfg; this.rng = mulberry32(c.seed); this.t = 0; this.frame = 0; this.events = []; this.state = 'run'; this.finaleT = null; this.winner = null;
      this.R = c.R; this.items = []; this.bombs = []; this.nextSpawn = c.firstSpawn; this.uid = 0;
      const n = c.fighters.length;
      this.balls = c.fighters.map((f, i) => { const a = -Math.PI / 2 + i * TAU / n + Math.PI / n * (n === 2 ? 1 : .5), d = this.inR() * .55, va = this.rng() * TAU;
        return { i, name: f.name, x: c.cx + Math.cos(a) * d, y: c.cy + Math.sin(a) * d, vx: Math.cos(va) * c.speed, vy: Math.sin(va) * c.speed, r: c.r, hp: c.hp, alive: true, w: null, shield: 0, boost: 0, hitCd: {}, flash: 0 }; });
    }
    inR() { return this.cfg.sides ? this.R * Math.cos(Math.PI / this.cfg.sides) : this.R; }
    ev(kind, o) { this.events.push(Object.assign({ t: +this.t.toFixed(4), kind }, o)); }
    get alive() { return this.balls.filter(b => b.alive); }
    wall(b, bounce = true) { const c = this.cfg, dx = b.x - c.cx, dy = b.y - c.cy; let nx, ny, pen = 0;
      if (c.sides) { const ap = this.R * Math.cos(Math.PI / c.sides); for (let k = 0; k < c.sides; k++) { const a = c.rot + (k + .5) * TAU / c.sides, ex = Math.cos(a), ey = Math.sin(a), p = dx * ex + dy * ey - (ap - b.r); if (p > pen) { pen = p; nx = ex; ny = ey; } } }
      else { const d = Math.hypot(dx, dy) || 1e-6, p = d - (this.R - b.r); if (p > 0) { pen = p; nx = dx / d; ny = dy / d; } }
      if (pen <= 0) return false; b.x -= nx * pen; b.y -= ny * pen; const vn = b.vx * nx + b.vy * ny;
      if (bounce && vn > 0) { b.vx -= 2 * vn * nx; b.vy -= 2 * vn * ny; const j = (this.rng() - .5) * .3, cs = Math.cos(j), sn = Math.sin(j), vx = b.vx * cs - b.vy * sn; b.vy = b.vx * sn + b.vy * cs; b.vx = vx; return true; } return false; }
    randPoint(margin) { for (let k = 0; k < 60; k++) { const a = this.rng() * TAU, d = Math.sqrt(this.rng()) * (this.inR() - margin), x = this.cfg.cx + Math.cos(a) * d, y = this.cfg.cy + Math.sin(a) * d;
        if (this.balls.every(b => !b.alive || Math.hypot(b.x - x, b.y - y) > b.r + 70)) return [x, y]; } return [this.cfg.cx, this.cfg.cy]; }
    weaponGeom(b) { const w = b.w, d = WEAPONS[w.type];
      if (d.disc) { const a = w.ang; return { disc: true, x: b.x + Math.cos(a) * (b.r + d.orbit), y: b.y + Math.sin(a) * (b.r + d.orbit), rad: d.rad }; }
      const a = d.point ? Math.atan2(b.vy, b.vx) : w.ang, ca = Math.cos(a), sa = Math.sin(a);
      return { ax: b.x + ca * (b.r + d.inner), ay: b.y + sa * (b.r + d.inner), bx: b.x + ca * (b.r + d.outer), by: b.y + sa * (b.r + d.outer), ang: a }; }
    damage(target, amount, from, kind, x, y) {
      if (!target.alive) return;
      if (target.shield > 0) { target.shield--; this.ev('block', { who: target.i, x, y }); return; }
      const dmg = Math.max(1, Math.round(amount * this.cfg.dmgScale)); target.hp = Math.max(0, target.hp - dmg); target.flash = 1;
      this.ev('hit', { who: target.i, by: from, v: dmg, w: kind, x: +x.toFixed(1), y: +y.toFixed(1) });
      if (target.hp <= 0) { target.alive = false; target.w = null; this.ev('ko', { who: target.i, by: from, x: target.x, y: target.y }); } }
    stepFrame() { const c = this.cfg, dt = 1 / c.fps / c.sub; for (let s = 0; s < c.sub; s++) this.substep(dt); this.frame++;
      if (this.state === 'run') { const al = this.alive; if (al.length <= 1 || this.t >= c.maxTime) { this.winner = (al.length ? al : this.balls).slice().sort((a, b) => b.hp - a.hp)[0].i; this.state = 'finale'; this.finaleT = this.t; this.ev('win', { who: this.winner }); } } }
    substep(dt) {
      const c = this.cfg; this.t += dt;
      if (c.shrinkFrom !== null && this.t > c.shrinkFrom) { const k = Math.min(1, (this.t - c.shrinkFrom) / c.shrinkDur); this.R = c.R + (c.shrinkTo - c.R) * k; }
      // spawns
      if (this.state === 'run' && this.t >= this.nextSpawn) { this.nextSpawn += c.spawnEvery * (.75 + this.rng() * .5);
        const type = c.pool[Math.floor(this.rng() * c.pool.length)], [x, y] = this.randPoint(70); this.items.push({ id: this.uid++, type, x, y, born: this.t }); this.ev('spawn', { w: type, x, y }); }
      this.items = this.items.filter(it => this.t - it.born < c.itemLife);
      for (const b of this.balls) { if (!b.alive) continue; const sp = c.speed * (b.boost > 0 ? 1.55 : 1); b.boost = Math.max(0, b.boost - dt); b.flash = Math.max(0, b.flash - dt * 4);
        const v = Math.hypot(b.vx, b.vy) || 1, k = 1 + .06 * (sp / v - 1); b.vx *= k; b.vy *= k; b.x += b.vx * dt; b.y += b.vy * dt;
        if (this.wall(b)) this.ev('wall', { who: b.i });
        for (const key in b.hitCd) b.hitCd[key] = Math.max(0, b.hitCd[key] - dt);
        if (b.w) { const d = WEAPONS[b.w.type]; b.w.ang += d.spin * dt * (b.i % 2 ? -1 : 1); b.w.left -= dt; if (b.w.left <= 0 || b.w.uses <= 0) { this.ev('drop', { who: b.i, w: b.w.type }); b.w = null; } } }
      // pickups
      for (const b of this.balls) { if (!b.alive || this.state !== 'run') continue;
        for (const it of this.items) { if (it.taken || Math.hypot(b.x - it.x, b.y - it.y) > b.r + 34) continue; it.taken = true;
          if (WEAPONS[it.type]) { b.w = { type: it.type, ang: Math.atan2(b.vy, b.vx), left: c.holdTime, uses: WEAPONS[it.type].uses }; }
          else if (it.type === 'heal') { const before = b.hp; b.hp = Math.min(c.hp, b.hp + 25); this.ev('heal', { who: b.i, v: b.hp - before, x: b.x, y: b.y }); }
          else if (it.type === 'shield') b.shield = 2;
          else if (it.type === 'speed') b.boost = 4;
          else if (it.type === 'bomb') this.bombs.push({ x: it.x, y: it.y, at: this.t + 1.0, owner: b.i });
          this.ev('pick', { who: b.i, w: it.type, x: it.x, y: it.y }); }
        this.items = this.items.filter(it => !it.taken); }
      // bombs
      for (const bm of this.bombs) if (!bm.done && this.t >= bm.at) { bm.done = true; this.ev('boom', { x: bm.x, y: bm.y, who: bm.owner });
        for (const f of this.balls) if (f.alive && f.i !== bm.owner) { const d = Math.hypot(f.x - bm.x, f.y - bm.y); if (d < 240) { this.damage(f, 26, bm.owner, 'bomb', f.x, f.y); const nx = (f.x - bm.x) / (d || 1), ny = (f.y - bm.y) / (d || 1); f.vx += nx * 900; f.vy += ny * 900; } } }
      this.bombs = this.bombs.filter(bm => !bm.done);
      // ball-ball
      const A = this.alive;
      for (let i = 0; i < A.length; i++) for (let j = i + 1; j < A.length; j++) { const a = A[i], b = A[j], dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy), min = a.r + b.r;
        if (d >= min || d < 1e-6) continue; const nx = dx / d, ny = dy / d, over = (min - d) / 2; a.x -= nx * over; a.y -= ny * over; b.x += nx * over; b.y += ny * over;
        const rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny; if (rv < 0) { a.vx += rv * nx; a.vy += rv * ny; b.vx -= rv * nx; b.vy -= rv * ny; this.ev('bump', { v: Math.min(1, -rv / 800) });
          if (this.state === 'run' && c.bump && !(a.hitCd['b' + b.i] > 0)) { a.hitCd['b' + b.i] = .5; this.damage(a, c.bump, b.i, 'bump', a.x + nx * a.r, a.y + ny * a.r); this.damage(b, c.bump, a.i, 'bump', b.x - nx * b.r, b.y - ny * b.r); } } }
      // weapon hits
      if (this.state === 'run') for (const h of this.alive) { if (!h.w) continue; const d = WEAPONS[h.w.type], G = this.weaponGeom(h);
        for (const f of this.alive) { if (f === h || (h.hitCd[f.i] > 0)) continue;
          const dist = G.disc ? Math.hypot(f.x - G.x, f.y - G.y) - G.rad : segDist(f.x, f.y, G.ax, G.ay, G.bx, G.by) - 6;
          if (dist < f.r) { h.hitCd[f.i] = d.cd; h.w.uses--; const nx = (f.x - h.x), ny = (f.y - h.y), l = Math.hypot(nx, ny) || 1; f.vx += nx / l * d.kb; f.vy += ny / l * d.kb;
            this.damage(f, d.dmg, h.i, h.w.type, f.x - nx / l * f.r, f.y - ny / l * f.r); if (!h.w) break; } } }
      if (this.state !== 'run') for (const b of this.balls) if (b.alive) this.wall(b);
    }
  }
  root.DuelSim = DuelSim; root.DUEL_WEAPONS = WEAPONS;
  if (typeof module !== 'undefined') module.exports = { DuelSim, WEAPONS };
})(typeof window !== 'undefined' ? window : globalThis);
