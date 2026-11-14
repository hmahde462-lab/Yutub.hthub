// Renders side-panel overlay (transparent PNG) + thumbnail for each compilation
const {chromium}=require('playwright');const fs=require('fs');
const C=JSON.parse(fs.readFileSync('comps.json'));
const E={};for(const f of ['../flag-battles/episodes.json','../flag-battles/episodes2.json'])for(const e of JSON.parse(fs.readFileSync(f)))E[e.n]=e;
const F=JSON.parse(fs.readFileSync('../facts-series/facts.json'));
const css=`<link rel=stylesheet href="../fonts/fonts.css"><style>
*{margin:0;box-sizing:border-box}body{width:1920px;height:1080px;background:transparent;font-family:Lalezar,Cairo;direction:rtl;color:#fff}
.p{position:absolute;top:0;width:656px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:26px;padding:40px}
.r{right:0}.l{left:0}.big{font-size:92px;line-height:1.05;text-shadow:0 6px 0 #0008}.mid{font-size:54px;text-shadow:0 4px 0 #0008}
.pill{background:var(--a);padding:10px 36px;border-radius:60px;font-size:50px;box-shadow:0 8px 0 #0006}.sm{font-size:40px;opacity:.95;text-shadow:0 3px 0 #0008}
</style>`;
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1920,height:1080}});
const path=require('path');const go=async h=>{fs.writeFileSync('tmp/p.html',h);await pg.goto('file://'+path.resolve('tmp/p.html'),{waitUntil:'networkidle'});await pg.evaluate(()=>document.fonts.ready);};
fs.mkdirSync('art',{recursive:true});
for(const c of C){
 const bat=c.kind==='battle';const acc=bat?'#e8322f':'#2f8fe8';
 const r=c.eps[0],s=c.eps[c.eps.length-1];
 const head=bat?'معارك الكرات':'معلومات غريبة';
 const sub=bat?`${c.eps.length} معارك نارية`:`${c.eps.length} دول`;
 const list=bat?c.eps.slice(0,4).map(n=>`${E[n].a} × ${E[n].b}`):c.eps.slice(0,5).map(n=>F[n-1].c);
 await go(`${css}<body style="--a:${acc}"><div class="p r"><div class=pill>تجميعة الأسبوع ${c.w}</div><div class=big>${head}</div><div class=mid>${sub}</div><div class=sm>الحلقات ${r} – ${s}</div></div>
 <div class="p l"><div class=mid>اكتب بالتعليقات</div><div class=big style="font-size:76px">${bat?'منو فاز بعينك؟':'إنت من وين؟'}</div><div class=pill>اشترك وفعّل الجرس</div><div class=sm>${bat?'معركة جديدة كل يوم':'معلومات جديدة كل يوم'}</div></div></body>`);
 await pg.screenshot({path:`art/${c.kind}-${c.w}-ov.png`,omitBackground:true});
 // thumbnail
 const bg=bat?'radial-gradient(circle at 50% 40%,#ff5a3c,#7a0b16 70%)':'radial-gradient(circle at 50% 40%,#3ca6ff,#0b2a7a 70%)';
 const fr=(i)=>'file://'+path.resolve(`art/fr-${c.kind}-${c.eps[i]}.jpg`);
 const center=bat?`<div style="font-size:120px">${E[r].a}<br><span style="color:#ffd400;font-size:150px">ضد</span><br>${E[r].b}</div>`:`<div style="font-size:110px;line-height:1.15">${list.slice(0,3).join('<br>')}</div>`;
 await go(`${css}<body style="--a:#ffd400;background:${bg};width:1920px;height:1080px"><img src="${fr(0)}" style="position:absolute;right:40px;top:90px;height:900px;transform:rotate(4deg);border:10px solid #fff;border-radius:30px;box-shadow:0 20px 40px #0009"><img src="${fr(1)}" style="position:absolute;left:40px;top:90px;height:900px;transform:rotate(-4deg);border:10px solid #fff;border-radius:30px;box-shadow:0 20px 40px #0009"><div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;text-shadow:0 10px 0 #0009;gap:30px">
 <div class=pill style="color:#111;font-size:80px;text-shadow:none">تجميعة الأسبوع</div>${center}<div class=mid style="font-size:70px">${bat?'+ '+(c.eps.length-1)+' معارك ثانية':'معلومات غريبة 🤯'.replace(' 🤯','')}</div></div></body>`);
 await pg.screenshot({path:`art/${c.kind}-${c.w}-thumb.jpg`,type:'jpeg',quality:82,scale:'css'});
}
await b.close();})();
