// Builds scenes.json: doodle paths + Arabic text shaped into glyph outlines (HarfBuzz).
const fs=require('fs');const {shape}=require('./shape.js');
const INK="#1d1d1f";
const C={red:"#e9483b",blue:"#2f7de1",orange:"#ff9f1c",green:"#21a366",pink:"#ff8fb1",yellow:"#ffd23f",sky:"#cfe8ff",gray:"#8d8d89",skin:"#ffe0c2",purple:"#c2185b"};
const circle=(cx,cy,r)=>`M${cx+r} ${cy} A${r} ${r} 0 1 1 ${cx-r} ${cy} A${r} ${r} 0 1 1 ${cx+r} ${cy}`;
const ellipse=(cx,cy,rx,ry)=>`M${cx+rx} ${cy} A${rx} ${ry} 0 1 1 ${cx-rx} ${cy} A${rx} ${ry} 0 1 1 ${cx+rx} ${cy}`;
const rrect=(x,y,w,h,r)=>`M${x+r} ${y} H${x+w-r} Q${x+w} ${y} ${x+w} ${y+r} V${y+h-r} Q${x+w} ${y+h} ${x+w-r} ${y+h} H${x+r} Q${x} ${y+h} ${x} ${y+h-r} V${y+r} Q${x} ${y} ${x+r} ${y} Z`;
const cloud=(cx,cy,s)=>`M${cx-1.2*s} ${cy+.4*s} Q${cx-1.55*s} ${cy-.05*s} ${cx-1.0*s} ${cy-.2*s} Q${cx-.9*s} ${cy-.8*s} ${cx-.3*s} ${cy-.6*s} Q${cx} ${cy-1.1*s} ${cx+.45*s} ${cy-.6*s} Q${cx+1.05*s} ${cy-.75*s} ${cx+1.0*s} ${cy-.15*s} Q${cx+1.55*s} ${cy} ${cx+1.2*s} ${cy+.4*s} Z`;
const drop=(x,y,s=1)=>`M${x} ${y-38*s} C${x+6*s} ${y-22*s} ${x+26*s} ${y-6*s} ${x+26*s} ${y+10*s} A${26*s} ${26*s} 0 0 1 ${x-26*s} ${y+10*s} C${x-26*s} ${y-6*s} ${x-6*s} ${y-22*s} ${x} ${y-38*s} Z`;
function rays(cx,cy,r1,r2,n,off=0){let d="";for(let i=0;i<n;i++){const a=off+i*2*Math.PI/n;d+=`M${(cx+r1*Math.cos(a)).toFixed(1)} ${(cy+r1*Math.sin(a)).toFixed(1)} L${(cx+r2*Math.cos(a)).toFixed(1)} ${(cy+r2*Math.sin(a)).toFixed(1)} `}return d}
function wave(x1,y,x2,amp=10,per=40){let d=`M${x1} ${y}`;for(let x=x1;x<x2;x+=per)d+=` q${per/4} ${-amp} ${per/2} 0 q${per/4} ${amp} ${per/2} 0`;return d}
function arrow(x1,y1,x2,y2,curve=0){const mx=(x1+x2)/2+curve,my=(y1+y2)/2-Math.abs(curve)*.3;const a=Math.atan2(y2-my,x2-mx),L=34;
  return `M${x1} ${y1} Q${mx} ${my} ${x2} ${y2} M${(x2-L*Math.cos(a-0.45)).toFixed(1)} ${(y2-L*Math.sin(a-0.45)).toFixed(1)} L${x2} ${y2} L${(x2-L*Math.cos(a+0.45)).toFixed(1)} ${(y2-L*Math.sin(a+0.45)).toFixed(1)}`}
function feather(x0,y0,x1,y1,cx,cy){let d=`M${x0} ${y0} Q${cx} ${cy} ${x1} ${y1}`;const N=11;
  for(let i=2;i<=N;i++){const t=i/(N+1);const px=(1-t)**2*x0+2*(1-t)*t*cx+t*t*x1,py=(1-t)**2*y0+2*(1-t)*t*cy+t*t*y1;
   const dx=2*(1-t)*(cx-x0)+2*t*(x1-cx),dy=2*(1-t)*(cy-y0)+2*t*(y1-cy),l=Math.hypot(dx,dy),nx=-dy/l,ny=dx/l;const len=70*Math.sin(Math.PI*Math.min(1,t*1.15));
   const f=v=>v.toFixed(1);
   d+=` M${f(px)} ${f(py)} q${f(nx*len*.5+dx/l*20)} ${f(ny*len*.5+dy/l*20)} ${f(nx*len+dx/l*45)} ${f(ny*len+dy/l*45)} M${f(px)} ${f(py)} q${f(-nx*len*.5+dx/l*20)} ${f(-ny*len*.5+dy/l*20)} ${f(-nx*len+dx/l*45)} ${f(-ny*len+dy/l*45)}`}return d}
const T=(txt,y,s,c,t0,t1,o={})=>({txt,y,s,c:c||INK,t0,t1,...o});
const P=(p,t0,t1,o={})=>({p,t0,t1,...o});

const bolt=(x,y,s=1)=>`M${x} ${y} l${20*s} ${-34*s} l${-6*s} ${22*s} l${24*s} ${-10*s} l${-22*s} ${34*s} l${6*s} ${-22*s} Z`;
const heart=(x,y,s=1)=>`M${x} ${y+26*s} C${x-40*s} ${y} ${x-28*s} ${y-30*s} ${x} ${y-12*s} C${x+28*s} ${y-30*s} ${x+40*s} ${y} ${x} ${y+26*s} Z`;
const grains=pts=>pts.map(([x,y])=>rrect(x-9,y-9,18,18,3)).join(" ");
const tree=(x,y)=>`M${x} ${y} L${x} ${y-90} `+circle(x,y-130,48);
const SCENES=[
 {name:"hook",els:[
  T("٥ أسئلة جديدة يسألها الطفل",330,100,INK,0,0,{pre:true}),
  P(rrect(820,560,200,74,37),0,0,{f:C.red,c:C.red,w:4,pre:true}),T("الجزء ٣",612,58,"#ffffff",0,0,{x:920,pre:true}),
  P(circle(330,930,150),0,0,{f:C.skin,w:9,pre:true}),
  P("M275 790 Q300 735 330 785 Q358 730 385 792",0,0,{w:9,pre:true}),
  P(circle(280,905,20),0,0,{f:INK,w:7,pre:true}),P(circle(382,905,20),0,0,{f:INK,w:7,pre:true}),
  P("M245 855 Q280 832 315 850 M347 850 Q382 832 417 855",0,0,{w:8,pre:true}),
  P(circle(330,1000,26),0,0,{f:"#c0392b",w:8,pre:true}),
  P("M250 1080 Q330 1110 410 1080 L450 1240 L210 1240 Z",0,0,{f:C.sky,w:9,pre:true}),
  T("؟",800,230,C.red,0,0,{x:135,rot:-12,pre:true}),
  // adult face drawn during "والكبار يسكتون"
  P(circle(760,930,165),0,0,{f:C.skin,w:9,pre:true}),
  P("M640 840 Q700 800 760 820 Q820 800 880 840",0,0,{w:9,pre:true}),
  P(circle(710,905,17),0,0,{f:INK,w:6,pre:true}),P(circle(810,905,17),0,0,{f:INK,w:6,pre:true}),
  P("M680 1010 L840 1010",.3,.38,{w:10}),
  P("M690 995 L690 1025 M712 995 L712 1025 M734 995 L734 1025 M756 995 L756 1025 M778 995 L778 1025 M800 995 L800 1025 M822 995 L822 1025",.38,.46,{w:6,c:C.gray}),
  P(drop(900,840,.8),.46,.52,{c:C.blue,w:6,f:C.sky}),
  P("M610 1100 Q760 1140 910 1100 L950 1240 L570 1240 Z",0,0,{f:"#ffd6a5",w:9,pre:true}),
  T("والكبار يحتارون!",470,116,C.red,.22,.5),
  T("جاهز؟ جاوب قبل الجواب!",1480,92,INK,.62,.88),
  P(wave(355,1560,895,9,46),.86,.96,{c:C.red,w:9})]},

 {name:"q1",q:1,els:[T("ليش السما تصير حمرة بالغروب؟",420,96,INK,.02,.16),
  P(rrect(90,600,900,640,30),.12,.18,{f:"#ffe1c4",w:6}),
  P("M90 820 L990 820 M90 940 L990 940",.16,.2,{c:"#ffb38a",w:28}),
  P("M90 1060 L990 1060",.18,.22,{c:"#ff7a59",w:34}),
  P("M90 1150 L990 1150",.2,.24,{w:8}),
  P("M420 1150 A120 120 0 0 1 660 1150 Z",.22,.3,{f:C.orange,w:8}),P(rays(540,1150,150,200,9,Math.PI),.28,.34,{c:C.orange,w:8}),
  P(arrow(640,1080,940,690,-80),.36,.44,{c:C.red,w:9}),
  P(circle(700,880,14)+" "+circle(760,770,12)+" "+circle(840,840,13)+" "+circle(620,760,11)+" "+circle(880,700,10),.44,.5,{f:C.blue,c:C.blue,w:4}),
  P(arrow(700,880,610,690,0)+arrow(840,840,980,760,0),.5,.56,{c:C.blue,w:5}),
  T("ضوء الشمس يقطع مسافة أطول",1440,82,C.orange,.4,.6),
  T("الأزرق يتشتت… ويوصلنا الأحمر!",1570,78,C.red,.66,.86)]},
 {name:"q2",q:2,els:[T("ليش القطة تطيح على رجليها؟",420,96,INK,.02,.16),
  P(ellipse(330,700,120,60),.12,.2,{f:C.orange,w:8}),P(circle(200,720,52),.18,.24,{f:C.orange,w:8}),
  P("M170 760 L160 800 L195 772 M230 760 L245 800 L212 772",.22,.26,{f:C.orange,w:6}),
  P("M270 650 L262 600 M320 642 L318 592 M370 642 L376 592 M410 650 L422 602",.24,.28,{w:9}),
  P("M450 700 Q520 640 500 600",.26,.3,{c:C.orange,w:10}),
  P(arrow(420,800,640,1060,160),.32,.42,{c:C.blue,w:9}),
  P(ellipse(760,1110,120,60),.42,.5,{f:C.orange,w:8}),P(circle(630,1080,52),.48,.54,{f:C.orange,w:8}),
  P("M600 1040 L590 1000 L625 1028 M660 1040 L675 1000 L642 1028",.52,.56,{f:C.orange,w:6}),
  P(circle(612,1074,7)+" "+circle(648,1074,7),.54,.57,{f:INK,w:3}),
  P("M700 1160 L692 1222 M750 1168 L748 1228 M800 1168 L806 1228 M840 1160 L852 1220",.56,.6,{w:9}),
  P("M880 1110 Q960 1060 940 1010",.58,.62,{c:C.orange,w:10}),
  P("M560 1240 L1000 1240",.6,.62,{c:C.green,w:8}),
  T("تلف راسها أول… وبعدين جسمها",1440,80,C.blue,.4,.6),
  T("فتنزل على رجليها!",1570,92,C.orange,.66,.86)]},
 {name:"q3",q:3,els:[T("ليش الزرافة رقبتها طويلة؟",420,98,INK,.02,.16),
  P("M840 1240 L840 760",.12,.16,{c:"#7a4a22",w:26}),P(cloud(840,700,150),.14,.22,{f:C.green,c:"#2b6b2b",w:8}),
  P(rrect(300,1000,240,120,40),.2,.28,{f:C.yellow,w:8}),
  P("M330 1120 L320 1240 M380 1120 L378 1240 M470 1120 L472 1240 M515 1120 L525 1240",.26,.3,{w:12}),
  P("M500 1020 L640 700 L680 720 L545 1035 Z",.3,.38,{f:C.yellow,w:8}),
  P(ellipse(690,690,62,36),.36,.42,{f:C.yellow,w:8}),P("M676 652 L670 620 M700 652 L706 620",.4,.43,{w:7}),P(circle(700,682,7),.42,.44,{f:INK,w:3}),
  P(circle(360,1040,14)+" "+circle(440,1070,12)+" "+circle(500,1030,11)+" "+circle(580,890,12)+" "+circle(620,800,10),.44,.48,{f:"#b5651d",c:"#7a3f10",w:3}),
  P("M745 690 Q770 680 790 700",.48,.52,{c:C.green,w:8}),
  P(ellipse(160,1180,70,42),.52,.56,{f:"#d9d9d9",w:7}),P(arrow(160,1120,160,980,0),.56,.6,{c:C.red,w:6}),
  P("M120 950 L200 1020 M200 950 L120 1020",.6,.63,{c:C.red,w:9}),
  T("توصل لأوراق الشجر العالية",1440,82,C.green,.4,.6),
  T("اللي باقي الحيوانات ما توصلها",1570,76,INK,.66,.86)]},
 {name:"q4",q:4,els:[T("ليش البرق قبل الرعد؟",420,104,INK,.02,.16),
  P(cloud(300,700,150),.12,.2,{f:"#9aa3ad",c:"#5a6068",w:8}),
  P(bolt(280,820,2.4),.2,.28,{f:C.yellow,c:C.orange,w:6}),
  P(ellipse(860,1060,46,70),.28,.34,{f:C.skin,w:8}),P("M846 1030 Q872 1060 846 1090",.32,.35,{w:6}),
  P(arrow(380,930,780,990,-40),.36,.42,{c:C.yellow,w:12}),
  P("M400 1140 A60 60 0 0 1 400 1240 M440 1110 A100 100 0 0 1 440 1270 M480 1080 A140 140 0 0 1 480 1300",.42,.56,{c:C.blue,w:8}),
  T("الضوء أسرع من الصوت",1440,92,C.orange,.4,.6),
  T("تقريباً مليون مرة!",1570,96,C.red,.66,.86)]},
 {name:"q5",q:5,els:[T("ليش الثلج أبيض؟",420,108,INK,.02,.16),
  P(rays(330,900,0,190,6,0),.12,.2,{c:"#7fb3e0",w:14}),
  P(rays(330,900,95,140,6,Math.PI/6),.18,.24,{c:"#7fb3e0",w:9}),
  P(circle(330,900,40),.22,.26,{f:"#ffffff",c:"#7fb3e0",w:8}),
  P(circle(300,840,10)+" "+circle(380,930,9)+" "+circle(290,960,8)+" "+circle(400,860,8),.26,.3,{f:"#ffffff",c:C.gray,w:3}),
  P(arrow(330,900,120,700,0)+arrow(330,900,560,700,0)+arrow(330,900,140,1140,0)+arrow(330,900,560,1120,0),.32,.42,{c:C.yellow,w:7}),
  P("M720 820 L760 1220 L940 1220 L980 820 Z",.42,.5,{w:8}),
  P(wave(730,900,970,10,60)+" M740 920 L960 920",.48,.52,{c:C.blue,w:6}),
  P(arrow(700,700,860,1100,0),.52,.58,{c:C.yellow,w:7}),
  T("الثلج بيه هوا محبوس",1440,96,C.blue,.4,.6),
  T("فيعكس الضوء بكل الاتجاهات",1570,80,INK,.66,.86)]},
 {name:"cta",els:[T("شكد جواب عرفت؟",400,104,INK,.0,.15),
  P(rrect(250,640,580,190,40),.12,.24,{f:C.red,w:10}),
  T("اشترك",770,130,"#ffffff",.24,.34,{stroke:"#ffffff"}),
  P("M880 690 Q880 620 940 610 Q1000 620 1000 690 L1012 760 L868 760 Z M920 772 Q940 800 960 772",.3,.38,{f:C.yellow,w:8}),
  P("M855 640 Q840 600 860 575 M1025 640 Q1040 600 1020 575",.37,.4,{c:C.orange,w:7}),
  P("M330 980 L330 870 Q330 845 352 845 Q374 845 374 870 L374 940 L374 900 Q374 880 394 880 Q414 880 414 905 L414 945 L414 915 Q414 895 434 895 Q454 895 454 920 L454 1000 Q454 1060 410 1080 L360 1080 Q320 1060 300 1010 L270 950 Q262 925 285 922 Q305 920 330 960",.4,.5,{f:"#fff",w:8}),
  T("بقناة أفكار غريبة",1230,104,C.blue,.36,.52),
  T("واكتبلي بالتعليقات:",1370,82,INK,.56,.68),
  T("شنو السؤال الجاي؟",1495,112,C.red,.68,.82),
  P(arrow(540,1570,540,1700,0),.82,.9,{c:C.red,w:10})]}
];
(async()=>{
  for(const sc of SCENES)for(const e of sc.els){if(e.txt&&e.y>=1380&&e.x===undefined){e.x=625;e.maxW=730;}}
  for(const sc of SCENES)for(const e of sc.els){if(!e.txt)continue;
    const font=e.font==='cairo'?'ttf/Cairo900.ttf':'ttf/Lalezar.ttf';
    let r=await shape(font,e.txt,e.s);
    const mw=e.maxW||960; if(r.width>mw){r=await shape(font,e.txt,e.s*mw/r.width)}
    e.width=r.width;e.sc=r.sc;e.glyphs=r.glyphs.map(g=>({d:g.d,x:g.x,y:g.y}));e.x=e.x??540;}
  fs.writeFileSync('scenes.json',JSON.stringify({SCENES,C}));console.log('ok',SCENES.length);
})();
