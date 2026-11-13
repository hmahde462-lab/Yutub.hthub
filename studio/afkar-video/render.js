const { chromium } = require('playwright');
const fs=require('fs'); const {spawn}=require('child_process');
const T=JSON.parse(fs.readFileSync('audio/tight.json'));
const tail=1.6, total=T.len+tail, b=T.bounds;
const times=[{start:0,end:b[0]}]; for(let i=0;i<b.length;i++) times.push({start:b[i],end:i+1<b.length?b[i+1]:total});
const mode=process.argv[2]||'preview';
(async()=>{
  const browser=await chromium.launch(); const page=await browser.newPage({viewport:{width:1080,height:1920}});
  await page.goto('file://'+__dirname+'/board.html'); await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(t=>window.setTimes(t),times);
  const stage=await page.$('#stage');
  if(mode==='preview'){
    const ts=process.argv.slice(3).map(Number);
    for(const t of ts){await page.evaluate(t=>renderAt(t),t); await stage.screenshot({path:`prev2/f_${t.toFixed(2)}.jpg`,type:'jpeg',quality:80});}
  } else {
    const fps=30, N=Math.round(total*fps);
    const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-i','audio/vo_tight.wav',
      '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','apad','-t',total.toFixed(3),'-movflags','+faststart','out/video.mp4'],{stdio:['pipe','inherit','inherit']});
    for(let i=0;i<N;i++){await page.evaluate(t=>renderAt(t),i/fps); const buf=await stage.screenshot({type:'jpeg',quality:92});
      if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); if(i%150===0) console.log('frame',i,'/',N);}
    ff.stdin.end(); await new Promise(r=>ff.on('close',r));
  }
  await browser.close(); console.log('total',total.toFixed(2),JSON.stringify(times));
})();
