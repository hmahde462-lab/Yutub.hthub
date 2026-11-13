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
  P(rrect(820,560,200,74,37),0,0,{f:C.red,c:C.red,w:4,pre:true}),T("الجزء ٤",612,58,"#ffffff",0,0,{x:920,pre:true}),
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


 {name:"q1",q:1,els:[T("ليش الخبز ينتفخ؟",420,108,INK,.02,.16),
  P("M180 1060 Q180 1240 400 1240 Q620 1240 620 1060 Z",.12,.2,{f:"#c98a4b",w:9}),
  P("M250 1060 Q260 990 400 985 Q540 990 550 1060 Z",.18,.24,{f:"#f3d9a4",w:8}),
  P(circle(330,1030,9)+" "+circle(400,1010,8)+" "+circle(470,1035,9),.22,.26,{f:"#8d6e63",w:3}),
  P(rrect(700,1150,70,70,8)+" "+rrect(790,1150,70,70,8),.26,.3,{f:"#ffffff",w:6}),
  P(circle(320,930,14)+" "+circle(400,890,20)+" "+circle(480,940,12)+" "+circle(440,830,16),.32,.38,{f:"#ffffff",c:C.blue,w:5}),
  P("M220 1060 Q210 820 400 790 Q590 820 580 1060 Z",.4,.48,{f:"#f3d9a4",w:9}),
  P(ellipse(810,760,90,110),.5,.56,{f:C.red,w:8}),P("M810 870 Q790 940 820 1000",.55,.58,{w:5}),
  P(arrow(600,900,710,800,-30),.58,.62,{c:C.orange,w:7}),
  T("الخميرة تاكل السكر وتطلّع غاز",1440,80,C.orange,.4,.6),
  T("والغاز ينفخ العجينة مثل البالون!",1570,76,INK,.66,.86)]},
 {name:"q2",q:2,els:[T("ليش البصمة تختلف؟",420,108,INK,.02,.16),
  P(ellipse(380,920,170,230),.12,.18,{f:C.skin,w:9}),
  P(ellipse(380,920,40,60)+" "+ellipse(380,920,80,110)+" "+ellipse(380,920,120,160)+" "+ellipse(380,920,155,205),.18,.32,{c:"#b07a5a",w:6}),
  P(circle(700,780,90),.32,.38,{c:C.gray,w:12}),P("M765 845 L860 940",.36,.4,{c:"#7a4a22",w:22}),
  P(circle(700,1120,45)+" "+circle(880,1120,45),.42,.48,{f:C.skin,w:7}),
  P("M640 1240 Q700 1170 760 1240 M820 1240 Q880 1170 940 1240",.46,.5,{f:C.sky,w:7}),
  P(wave(670,1110,730,8,20)+" "+"M850 1100 Q880 1140 910 1100",.5,.56,{c:C.red,w:5}),
  T("≠",1060,90,C.red,.55,.58,{x:790,font:"cairo"}),
  T("تتشكل واحنا ببطن الأم",1440,90,C.blue,.4,.6),
  T("حتى التوائم بصماتهم مختلفة!",1570,80,C.red,.66,.86)]},
 {name:"q3",q:3,els:[T("ليش السفينة ما تغرق؟",420,104,INK,.02,.16),
  P("M80 1060 L1000 1060 L1000 1260 L80 1260 Z",.12,.18,{f:C.sky,c:C.blue,w:4}),
  P(wave(90,1060,990,12,60),.16,.22,{c:C.blue,w:8}),
  P("M260 1000 L820 1000 L740 1110 L340 1110 Z",.22,.3,{f:"#8d99a6",w:9}),
  P("M330 1010 L760 1010 L715 1080 L375 1080 Z",.3,.36,{f:"#eef6ff",c:C.gray,w:4}),
  P("M520 1000 L520 760 M520 780 L700 900 L520 900",.34,.4,{w:8}),
  P(arrow(420,1250,420,1130,0)+arrow(540,1250,540,1130,0)+arrow(660,1250,660,1130,0),.44,.52,{c:C.blue,w:8}),
  P(arrow(900,840,900,980,0),.52,.56,{c:C.red,w:7}),
  T("مجوفة ومليانة هوا",1440,96,C.blue,.4,.6),
  T("والماي يدفعها لفوك!",1570,92,INK,.66,.86)]},
 {name:"q4",q:4,els:[T("ليش نسد عيوننا بالعطسة؟",420,98,INK,.02,.16),
  P(circle(380,940,170),.12,.2,{f:C.skin,w:9}),
  P("M300 900 Q330 870 360 900 M400 900 Q430 870 460 900",.2,.26,{w:8}),
  P("M330 1010 Q380 1050 430 1010",.24,.28,{w:7}),
  P(drop(600,960,.5)+" "+drop(660,900,.45)+" "+drop(650,1020,.4)+" "+drop(720,960,.5),.28,.36,{c:C.blue,w:5,f:C.sky}),
  T("آچوو!",760,120,C.red,.3,.38,{x:780}),
  P(cloud(380,640,95),.42,.5,{f:C.pink,w:7}),P("M330 640 Q380 600 430 640 M340 670 Q380 640 420 670",.48,.52,{c:"#c2185b",w:5}),
  P(arrow(380,730,370,860,0),.52,.58,{c:C.purple,w:7}),
  T("رد فعل تلقائي",1440,100,C.purple,.4,.6),
  T("والدماغ يسد العيون بدون ما نحس",1570,74,INK,.66,.86)]},
 {name:"q5",q:5,els:[T("ليش الشمس تبين صغيرة؟",420,102,INK,.02,.16),
  P("M80 600 A420 420 0 0 1 80 1260",.12,.22,{f:C.yellow,c:C.orange,w:9}),
  P("M305.0 540.3 L330.0 497.0 M424.7 640.7 L463.0 608.6 M502.9 776.1 L549.8 759.0 M530.0 930.0 L580.0 930.0 M502.9 1083.9 L549.8 1101.0 M424.7 1219.3 L463.0 1251.4 M305.0 1319.7 L330.0 1363.0",.2,.26,{c:C.orange,w:7}),
  P(circle(900,930,22),.28,.32,{f:C.blue,c:"#1b4f9c",w:6}),P("M890 925 q8 -10 16 0",.31,.33,{c:C.green,w:5}),
  P("M540 1060 L860 1060",.36,.46,{c:INK,w:6}),P(arrow(560,1060,540,1060,0)+arrow(840,1060,870,1060,0),.44,.48,{w:6}),
  T("١٥٠ مليون كم",1140,76,C.red,.46,.56,{x:700}),
  T("أكبر من الأرض بمية مرة!",1440,90,C.orange,.4,.6),
  T("بس بعيدة جداً… فتبين صغيرة",1570,80,INK,.66,.86)]},
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
