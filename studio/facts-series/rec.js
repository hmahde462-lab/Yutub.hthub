// node rec.js <n> <segdir> video out.mp4 | preview t1 t2 ...   (also writes <segdir>/timeline.json)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const n = +process.argv[2], dir = process.argv[3], mode = process.argv[4]; const FPS = 30;
const E = JSON.parse(fs.readFileSync(path.join(__dirname, 'facts.json'), 'utf8'))[n - 1]; const S = JSON.parse(fs.readFileSync(path.join(dir, 'segs.json'), 'utf8'));
const EP = { n, c: E.c, f: E.f, x: E.x, durs: S.durs };
const built = path.join(__dirname, `.built_${n}.html`); fs.writeFileSync(built, fs.readFileSync(path.join(__dirname, 'facts.html'), 'utf8').replace('__EP__', JSON.stringify(EP)));
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + built);
  await p.evaluate(() => Promise.all([document.fonts.load("70px 'Lalezar'", 'ا1'), document.fonts.load("900 42px 'Cairo'", 'اAa1'), document.fonts.load("80px 'Noto Color Emoji'", '🇯🇵🐶'), document.fonts.ready]));
  const stage = await p.$('#stage'); const tl = await p.evaluate(() => timeline()); fs.writeFileSync(path.join(dir, 'timeline.json'), JSON.stringify(tl));
  if (mode === 'preview') { for (const ts of process.argv.slice(5)) { await p.evaluate(t => renderAt(t), Number(ts)); await stage.screenshot({ path: path.join(dir, `prev_${ts}.jpg`), type: 'jpeg', quality: 80 }); } }
  else { const out = process.argv[5], N = Math.round(tl.total * FPS);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < N; i++) { await p.evaluate(t => renderAt(t), i / FPS); const buf = await stage.screenshot({ type: 'jpeg', quality: 88 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  console.log('facts', n, E.c, 'total', tl.total.toFixed(1), errs.length ? 'ERRORS ' + errs.slice(0, 3) : 'ok'); await b.close(); })();
