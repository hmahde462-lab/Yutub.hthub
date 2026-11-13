// node rec.js <n> preview t1 t2 ... | <n> video out.mp4 | <n> events out.json
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const n = +process.argv[2], mode = process.argv[3]; const EP = [...JSON.parse(fs.readFileSync(path.join(__dirname, 'episodes.json'), 'utf8')), ...(fs.existsSync(path.join(__dirname, 'episodes2.json')) ? JSON.parse(fs.readFileSync(path.join(__dirname, 'episodes2.json'), 'utf8')) : [])].find(e => e.n === n); const FPS = 30;
const built = path.join(__dirname, `.built_${n}.html`); fs.writeFileSync(built, fs.readFileSync(path.join(__dirname, 'flagduel.html'), 'utf8').replace('__EP__', JSON.stringify(EP)));
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + built);
  await p.evaluate(() => Promise.all([document.fonts.load("70px 'Lalezar'", 'ا1'), document.fonts.load("900 42px 'Cairo'", 'اAa1'), document.fonts.ready]));
  const stage = await p.$('#stage'); const total = await p.evaluate(() => getTotal());
  if (mode === 'events') fs.writeFileSync(process.argv[4], JSON.stringify(await p.evaluate(() => allEvents())));
  else if (mode === 'preview') { fs.mkdirSync('out/prev', { recursive: true }); for (const ts of process.argv.slice(4)) { await p.evaluate(t => renderAt(t), Number(ts)); await stage.screenshot({ path: `out/prev/${n}_${ts}.jpg`, type: 'jpeg', quality: 80 }); } }
  else { const out = process.argv[4], N = Math.round(total * FPS);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < N; i++) { await p.evaluate(t => renderAt(t), i / FPS); const buf = await stage.screenshot({ type: 'jpeg', quality: 88 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  console.log('ep', n, 'total', total.toFixed(1), errs.length ? 'ERRORS ' + errs.slice(0, 3) : 'ok'); await b.close(); })();
