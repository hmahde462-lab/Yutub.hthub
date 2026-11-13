// node rec.js top10.json [preview t1 t2 ...]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const CFG = JSON.parse(fs.readFileSync(process.argv[2])); const mode = process.argv[3] || 'full';
const built = path.join(__dirname, '.built.html'); fs.writeFileSync(built, fs.readFileSync(path.join(__dirname, 'top10.html'), 'utf8').replace('__CFG__', JSON.stringify(CFG)));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + built);
  await p.evaluate(() => Promise.all([document.fonts.load("70px 'Lalezar'", 'ا1'), document.fonts.load("900 42px 'Cairo'", 'اAa1'), document.fonts.ready]));
  const stage = await p.$('#stage'); fs.mkdirSync('out/prev', { recursive: true });
  if (mode === 'preview') {
    for (const ts of process.argv.slice(4)) { await p.evaluate(i => { seek(i); frame(); }, Math.round(Number(ts) * CFG.fps)); if (errs.length) { console.log('ERR', errs[0]); break; } await stage.screenshot({ path: `out/prev/${ts}.jpg`, type: 'jpeg', quality: 80 }); }
  } else {
    const N = Math.round(CFG.end * CFG.fps);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(CFG.fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', 'out/video.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < N; i++) { await p.evaluate(() => frame()); if (errs.length) { console.log('ERR', errs[0]); break; }
      const buf = await stage.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 300 === 0) console.log('frame', i, '/', N); }
    fs.writeFileSync('out/events.json', JSON.stringify({ duration: CFG.end, events: await p.evaluate(() => getEvents()) }));
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close(); console.log('done', errs.length ? 'ERR' : 'ok');
})();
