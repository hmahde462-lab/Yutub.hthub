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
  P(rrect(820,560,200,74,37),0,0,{f:C.red,c:C.red,w:4,pre:true}),T("الجزء ٢",612,58,"#ffffff",0,0,{x:920,pre:true}),
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
 {name:"q1",q:1,els:[T("ليش البحر مالح؟",420,104,INK,.02,.16),
  P("M100 1010 L300 700 L500 1010 Z",.14,.22,{f:"#b8a48a",w:9}),
  P("M320 760 Q340 880 430 935 Q520 990 620 1020",.2,.28,{c:C.blue,w:12}),
  P(grains([[350,830],[445,945],[560,1005]]),.26,.32,{f:"#ffffff",w:4}),
  P("M560 1040 L1010 1040 L1010 1250 L560 1250 Z",.28,.34,{f:C.sky,c:C.blue,w:4}),
  P(wave(570,1080,1000,14,70)+wave(570,1140,1000,14,70)+wave(570,1200,1000,14,70),.3,.38,{c:C.blue,w:8}),
  P(circle(850,700,70),.34,.4,{f:C.yellow,w:9}),P(rays(850,700,98,140,10,.2),.38,.44,{c:C.orange,w:9}),
  P(arrow(660,1030,660,880,0)+arrow(800,1030,800,860,0)+arrow(930,1030,930,890,0),.44,.52,{c:C.blue,w:7}),
  P(grains([[740,1225],[760,1205],[780,1225],[800,1205],[820,1225]]),.52,.58,{f:"#ffffff",w:4}),
  T("الأنهار تجيب الملح من الصخور",1440,82,C.blue,.4,.6),
  T("والشمس تبخّر الماي… والملح يبقى!",1570,76,INK,.66,.86)]},
 {name:"q2",q:2,els:[T("ليش البصل يبچينا؟",420,104,INK,.02,.16),
  P("M420 1220 C300 1220 280 1070 340 1000 C380 950 420 920 420 870 C420 920 460 950 500 1000 C560 1070 540 1220 420 1220 Z",.12,.24,{f:"#c77dbf",w:9}),
  P("M420 880 C400 980 360 1100 380 1210 M420 880 C440 980 480 1100 460 1210",.22,.28,{c:"#7a2f6f",w:5}),
  P("M560 960 L760 820 L780 850 L600 1000 Z",.26,.32,{f:"#d9d9d9",w:7}),P("M760 820 L860 750 L880 780 L780 850 Z",.3,.34,{f:"#7a4a22",w:7}),
  P("M470 900 q24 -40 0 -80 t0 -80 M530 920 q24 -40 4 -80 t4 -80",.34,.44,{c:C.green,w:8}),
  P("M560 650 Q680 560 800 650 Q680 740 560 650 Z",.42,.48,{f:"#ffffff",w:8}),P(circle(680,650,34),.46,.5,{f:"#5b3a1e",w:6}),P(circle(680,650,14),.49,.52,{f:INK,w:4}),
  P(drop(640,745,.8),.52,.56,{c:C.blue,w:6,f:C.sky}),P(drop(722,775,.7),.55,.59,{c:C.blue,w:6,f:C.sky}),
  T("يطلع غاز يوصل لعيوننا",1440,84,C.green,.4,.6),
  T("فالعين تغسله بالدموع!",1570,84,C.blue,.66,.86)]},
 {name:"q3",q:3,els:[T("ليش الطيور ما تتكهرب؟",420,100,INK,.02,.16),
  P("M140 1260 L140 760 M940 1260 L940 760",.12,.2,{c:"#7a4a22",w:16}),P("M95 790 L185 790 M895 790 L985 790",.18,.22,{c:"#7a4a22",w:12}),
  P("M140 800 Q540 900 940 800",.2,.28,{w:6}),
  P("M485 815 Q500 770 545 775 Q600 780 595 830 Q570 860 520 855 Q480 850 485 815 Z",.28,.34,{f:"#3f8fd1",w:6}),
  P(circle(600,770,26),.32,.36,{f:"#3f8fd1",w:6}),P("M622 768 L656 778 L622 788 Z",.35,.37,{f:C.orange,w:4}),P(circle(606,764,5),.36,.37,{f:INK,w:3}),
  P("M500 820 Q540 790 575 822 Q540 838 500 820 Z",.36,.39,{f:"#2a6db0",w:4}),P("M530 856 L526 872 M556 856 L560 872",.38,.4,{w:5}),
  P(bolt(240,840)+" "+bolt(370,870)+" "+bolt(700,872)+" "+bolt(830,840),.4,.48,{f:C.yellow,c:C.orange,w:4}),
  P(arrow(300,950,780,950,0),.5,.56,{c:C.orange,w:7}),
  T("واقفة على سلك واحد",1440,90,C.blue,.4,.58),
  T("فالكهرباء ما تمر بجسمها",1570,84,INK,.64,.86)]},
 {name:"q4",q:4,els:[T("ليش القمر يلحقنا؟",420,104,INK,.02,.16),
  P(circle(820,650,80),.12,.2,{f:"#fff7c2",w:8}),P(circle(795,630,13)+" "+circle(845,680,9)+" "+circle(840,620,7),.18,.22,{c:"#c9b25a",w:4}),
  P(rays(180,620,0,22,4,0)+rays(330,700,0,16,4,0)+rays(600,560,0,18,4,0),.2,.26,{c:C.yellow,w:6}),
  P("M60 1230 L1020 1230",.22,.26,{w:8}),P(tree(150,1230)+" "+tree(930,1230),.24,.32,{f:C.green,c:"#2b6b2b",w:7}),
  P(rrect(300,1100,300,90,30)+" M360 1100 L400 1040 L520 1040 L560 1100",.3,.38,{f:C.red,w:8}),P(circle(370,1196,30)+" "+circle(530,1196,30),.36,.4,{f:INK,w:5}),
  P("M450 1040 L800 660",.42,.48,{c:C.orange,w:6}),
  P(rrect(620,1100,300,90,30),.48,.52,{c:C.gray,w:5}),P("M770 1040 L830 665",.5,.56,{c:C.orange,w:6}),
  T("القمر بعيد جدًا",1440,96,C.orange,.4,.58),
  T("فمكانه ما يتغير… ونحس يلحقنا!",1570,78,INK,.64,.86)]},
 {name:"q5",q:5,els:[T("ليش نحلم؟",420,112,INK,.02,.14),
  P("M250 1190 Q230 1110 320 1100 L720 1100 Q810 1110 790 1190 Q720 1220 320 1220 Q240 1220 250 1190 Z",.12,.2,{f:"#ffffff",w:8}),
  P(circle(420,1040,110),.18,.28,{f:C.skin,w:9}),P("M365 1030 Q385 1046 405 1030 M435 1030 Q455 1046 475 1030",.28,.32,{w:7}),P("M395 1085 Q420 1100 445 1085",.3,.33,{w:6}),
  T("Z",880,90,C.blue,.32,.35,{x:560,font:"cairo"}),T("z",820,66,C.blue,.35,.38,{x:600,font:"cairo"}),
  P(circle(585,915,18)+" "+circle(640,850,28),.38,.44,{f:"#ffffff",w:6}),P(cloud(790,690,150),.42,.5,{f:"#ffffff",w:8}),
  P(heart(720,690,1.1),.5,.54,{f:C.red,w:5}),P(circle(840,700,34),.53,.57,{f:C.orange,w:5}),P(rays(785,620,0,22,5,0),.56,.6,{c:C.yellow,w:6}),
  T("العلماء مو متأكدين!",1440,100,C.red,.4,.56),
  T("يمكن الدماغ يرتب ذكرياتنا",1570,80,C.blue,.64,.86)]},
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
