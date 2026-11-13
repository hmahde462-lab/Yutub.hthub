// usage: node record.js episodes/ep01.json [preview t1 t2 ...]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const epPath = process.argv[2], mode = process.argv[3] || 'full', EP = JSON.parse(fs.readFileSync(epPath));
const html = fs.readFileSync(path.join(__dirname, EP.template || 'render.html'), 'utf8').replace('__EP__', JSON.stringify(EP));
const built = path.join(__dirname, `.built_${EP.id}.html`); fs.writeFileSync(built, html);
const TAIL = 3.6, FPS = 60;
(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + built); await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([document.fonts.load("84px 'Lalezar'", 'ا'), document.fonts.load("900 50px 'Cairo'", 'ا'), document.fonts.load("900 50px 'Cairo'", '0123456789')]));
  const stage = await page.$('#stage');
  const want = mode === 'preview' ? new Set(process.argv.slice(4).map(t => Math.round(Number(t) * FPS))) : null;
  let ff = null;
  if (!want) ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', `out/${EP.id}_video.mp4`], { stdio: ['pipe', 'inherit', 'inherit'] });
  fs.mkdirSync('out/prev', { recursive: true });
  let i = 0, st;
  while (true) {
    st = await page.evaluate(() => frame());
    if (want) { if (want.has(i)) await stage.screenshot({ path: `out/prev/${EP.id}_${(i / FPS).toFixed(2)}.jpg`, type: 'jpeg', quality: 80 }); if (i >= Math.max(...want)) break; }
    else { const buf = await stage.screenshot({ type: 'jpeg', quality: 92 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 300 === 0) console.log('frame', i, 't', st.t.toFixed(1), 'n', st.n); }
    i++;
    const info = await page.evaluate(() => getInfo());
    if (info.finaleT !== null && st.t > info.finaleT + TAIL) break;
    if (i > 60 * 70) break;
  }
  const info = await page.evaluate(() => getInfo()); const events = await page.evaluate(() => getEvents());
  fs.writeFileSync(`out/${EP.id}_events.json`, JSON.stringify({ fps: FPS, frames: i, duration: i / FPS, info, events }));
  if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await browser.close(); console.log('done frames', i, 'duration', (i / FPS).toFixed(2), JSON.stringify(info), 'events', events.length);
})();
