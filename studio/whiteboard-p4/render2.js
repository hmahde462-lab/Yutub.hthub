const { chromium } = require('playwright');const fs=require('fs');const {spawn}=require('child_process');
const T=JSON.parse(fs.readFileSync('audio/tight.json'));const SH=0.3;
const tail=1.6,total=T.len+SH+tail,b=T.bounds.map(x=>x+SH);
const times=[{start:0,end:b[0]}];for(let i=0;i<b.length;i++)times.push({start:b[i],end:i+1<b.length?b[i+1]:total});
const mode=process.argv[2]||'preview',fps=30;
(async()=>{const browser=await chromium.launch();const page=await browser.newPage({viewport:{width:1080,height:1920}});
 await page.goto('file://'+__dirname+'/board2_built.html');await page.evaluate(()=>document.fonts.ready);
 await page.evaluate(t=>window.setTimes(t),times);const stage=await page.$('#stage');
 if(mode==='preview'){fs.mkdirSync('prev3',{recursive:true});const ts=process.argv.slice(3).map(Number);const maxT=Math.max(...ts);
   const want=new Set(ts.map(t=>Math.round(t*fps)));
   for(let i=0;i<=Math.round(maxT*fps);i++){await page.evaluate(t=>renderAt(t),i/fps);
     if(want.has(i))await stage.screenshot({path:`prev3/f_${(i/fps).toFixed(2)}.jpg`,type:'jpeg',quality:80});}
 } else {const N=Math.round(total*fps);const stats=[];
   const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','out/video_noaudio.mp4'],{stdio:['pipe','inherit','inherit']});
   for(let i=0;i<N;i++){stats.push(await page.evaluate(t=>renderAt(t),i/fps));const buf=await stage.screenshot({type:'jpeg',quality:93});
     if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log('frame',i,'/',N);}
   ff.stdin.end();await new Promise(r=>ff.on('close',r));fs.writeFileSync('out/stats.json',JSON.stringify({fps,total,stats}));}
 await browser.close();console.log('total',total.toFixed(2));})();
