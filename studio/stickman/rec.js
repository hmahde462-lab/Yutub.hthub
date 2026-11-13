// node rec.js <cfg.json> [preview t1 t2 ...]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const cfgPath = process.argv[2], mode = process.argv[3] || 'full', CFG = JSON.parse(fs.readFileSync(cfgPath));
const html = fs.readFileSync(path.join(__dirname, 'story.html'), 'utf8').replace('__CFG__', JSON.stringify(CFG));
const built = path.join(__dirname, `.built_${CFG.id}.html`); fs.writeFileSync(built, html);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + built);
  await p.evaluate(() => Promise.all([document.fonts.load("70px 'Lalezar'", 'ا'), document.fonts.load("900 42px 'Cairo'", 'Aa'), document.fonts.ready]));
  const stage = await p.$('#stage'), FPS = CFG.fps, N = Math.round(CFG.end * FPS);
  const want = mode === 'preview' ? new Set(process.argv.slice(4).map(t => Math.round(Number(t) * FPS))) : null;
  let ff = null; fs.mkdirSync('out/prev', { recursive: true });
  if (!want) ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', `out/${CFG.id}_video.mp4`], { stdio: ['pipe', 'inherit', 'inherit'] });
  const last = want ? Math.max(...want) : N - 1;
  for (let i = 0; i <= last; i++) {
    await p.evaluate(() => frame());
    if (errs.length) { console.log('PAGE ERROR', errs[0]); break; }
    if (want) { if (want.has(i)) await stage.screenshot({ path: `out/prev/${(i / FPS).toFixed(1)}.jpg`, type: 'jpeg', quality: 80 }); }
    else { const buf = await stage.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 300 === 0) console.log('frame', i, '/', N); }
  }
  fs.writeFileSync(`out/${CFG.id}_events.json`, JSON.stringify({ duration: CFG.end, events: await p.evaluate(() => getEvents()) }));
  if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await b.close(); console.log('done', errs.length ? 'with errors' : 'ok');
})();
