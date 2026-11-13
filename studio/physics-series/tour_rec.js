// node tour_rec.js preview t1 t2 ... | chunk <f0> <f1> <out.mp4> | events
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const TOUR = fs.readFileSync(path.join(__dirname, 'episodes/tour1.json'), 'utf8'); const FPS = 30;
const built = path.join(__dirname, '.built_tour.html'); fs.writeFileSync(built, fs.readFileSync(path.join(__dirname, 'tour.html'), 'utf8').replace('__TOUR__', TOUR));
(async () => { const mode = process.argv[2]; const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + built);
  await p.evaluate(() => Promise.all([document.fonts.load("70px 'Lalezar'", 'ا1'), document.fonts.load("900 42px 'Cairo'", 'اAa1'), document.fonts.ready]));
  const stage = await p.$('#stage'); const total = await p.evaluate(() => getTotal());
  if (mode === 'events') { fs.writeFileSync('out/tour1_events.json', JSON.stringify(await p.evaluate(() => allEvents()))); console.log('events ok total', total.toFixed(1)); }
  else if (mode === 'preview') { fs.mkdirSync('out/prev', { recursive: true }); for (const ts of process.argv.slice(3)) { await p.evaluate(t => renderAt(t), Number(ts)); await stage.screenshot({ path: `out/prev/tour_${ts}.jpg`, type: 'jpeg', quality: 80 }); } console.log('total', total.toFixed(1)); }
  else { const f0 = +process.argv[3], f1 = Math.min(+process.argv[4], Math.round(total * FPS)), out = process.argv[5];
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = f0; i < f1; i++) { await p.evaluate(t => renderAt(t), i / FPS); const buf = await stage.screenshot({ type: 'jpeg', quality: 90 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('chunk done', f0, f1); }
  if (errs.length) console.log('PAGE ERRORS', errs.slice(0, 3)); await b.close(); })();
