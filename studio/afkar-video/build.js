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
const SCENES=[
 {name:"hook",els:[
  T("٥ أسئلة يسألها أي طفل",330,104,INK,0,0,{pre:true}),
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
  T("والكبار يسكتون!",470,118,C.red,.22,.5),
  T("انت تعرف جوابها؟",1480,100,INK,.62,.88),
  P(wave(270,1560,810,9,46),.86,.96,{c:C.red,w:9})]},
 {name:"q1",q:1,els:[T("ليش السما زرقاء؟",420,104,INK,.02,.16),
  P(cloud(320,760,105),.14,.24,{f:"#fff",w:9}),
  P(circle(800,760,92),.16,.26,{f:C.yellow,w:9}),P(rays(800,760,122,172,10,.2),.24,.32,{c:C.orange,w:10}),
  P("M730 830 L560 1000",.3,.36,{c:"#d6d6d1",w:26}),
  P(arrow(545,1010,400,930,-30),.36,.41,{c:C.blue,w:9}),P(arrow(545,1010,470,860,20),.39,.44,{c:C.blue,w:9}),
  P(arrow(545,1010,690,940,-20),.42,.47,{c:C.blue,w:9}),P(arrow(545,1010,420,1080,10),.45,.5,{c:C.blue,w:9}),
  P("M560 1000 L640 1160",.47,.5,{c:C.orange,w:7,dash:1}),
  P(wave(110,1250,980,14,80),.4,.5,{w:9}),
  P(circle(250,1130,32)+" M250 1162 L250 1236 M250 1186 L212 1212 M250 1186 L288 1212",.48,.56,{w:8}),
  T("الأزرق يتشتت أكثر",1440,100,C.blue,.48,.68),
  T("فنشوفه بكل مكان",1570,80,INK,.7,.86)]},
 {name:"q2",q:2,els:[T("ليش ما نكدر ندغدغ نفسنا؟",420,88,INK,.02,.17),
  P(cloud(330,830,140),.15,.27,{f:C.pink,w:9}),
  P("M240 820 q30 -40 60 0 t60 0 t60 0 M260 880 q30 -30 60 0 t60 0",.26,.33,{c:C.purple,w:7}),
  P("M300 650 l-20 -45 M340 640 l0 -50 M380 650 l20 -45",.3,.34,{c:C.orange,w:9}),
  P(arrow(500,820,640,900,40),.34,.42,{w:9}),
  P(feather(650,1180,890,760,760,1020),.4,.55,{c:C.blue,w:7}),
  T("ههههه",1250,84,C.gray,.55,.62,{x:770}),
  P("M650 1205 L890 1300 M890 1205 L650 1300",.62,.67,{c:C.red,w:12}),
  T("دماغك يعرف حركتك قبل لا تصير",1450,74,C.purple,.4,.62),
  T("والدغدغة تحتاج مفاجأة!",1575,86,INK,.7,.88)]},
 {name:"q3",q:3,els:[T("ليش نتثاوب؟",420,112,INK,.02,.14),
  P(circle(500,900,210),.12,.28,{f:C.skin,w:9}),
  P("M400 830 Q435 855 470 830 M530 830 Q565 855 600 830",.27,.32,{w:9}),
  P(ellipse(500,990,62,88),.31,.38,{f:"#8e2a2a",w:9}),
  P("M310 900 Q270 920 310 960",.36,.39,{w:9}),
  T("Z",700,120,C.blue,.38,.41,{x:760,font:"cairo"}),T("z",610,90,C.blue,.41,.44,{x:830,font:"cairo"}),
  P(rrect(800,860,60,230,30)+" "+circle(830,1130,52),.44,.52,{f:"#fff",w:8}),
  P("M830 1110 V940",.52,.58,{c:C.blue,w:24}),P(circle(830,1130,34),.5,.54,{c:C.blue,w:8,f:C.blue}),
  T("العلماء لحد هسه",1390,88,INK,.36,.52),
  T("مو متأكدين!",1515,120,C.red,.52,.66),
  T("يمكن حتى نبرّد الدماغ",1645,74,C.blue,.72,.9)]},
 {name:"q4",q:4,els:[T("ليش أصابعنا تتجعد بالماي؟",420,90,INK,.02,.17),
  P(rrect(380,960,330,300,70),.12,.22,{f:C.skin,w:9}),
  P(rrect(385,700,70,300,35),.2,.25,{f:C.skin,w:9}),P(rrect(465,650,70,340,35),.23,.28,{f:C.skin,w:9}),
  P(rrect(545,670,70,320,35),.26,.31,{f:C.skin,w:9}),P(rrect(625,730,70,270,35),.29,.34,{f:C.skin,w:9}),
  P("M380 1060 Q300 1010 280 940 Q270 900 310 905 Q350 915 400 1000",.32,.37,{f:C.skin,w:9}),
  P(wave(398,745,442,6,14)+wave(398,775,442,6,14)+wave(478,695,522,6,14)+wave(478,725,522,6,14)+wave(558,715,602,6,14)+wave(558,745,602,6,14)+wave(638,775,682,6,14)+wave(638,805,682,6,14),.4,.5,{c:"#b5651d",w:5}),
  P(drop(270,760),.36,.4,{c:C.blue,w:7,f:C.sky}),P(drop(820,700,1.2),.38,.42,{c:C.blue,w:7,f:C.sky}),P(drop(840,1000,.9),.4,.44,{c:C.blue,w:7,f:C.sky}),
  T("مو لأنها تشرب ماي!",1390,90,C.red,.34,.5),
  T("إشارة من الأعصاب",1515,104,C.blue,.52,.66),
  T("حتى نمسك المبلول بقوة",1640,76,INK,.72,.88)]},
 {name:"q5",q:5,els:[T("الدجاجة لو البيضة؟",420,104,INK,.02,.16),
  P(circle(300,940,120)+" "+circle(370,800,62),.12,.24,{f:"#fff",w:9}),
  P("M425 790 L470 808 L425 825 Z",.22,.25,{f:C.orange,w:8}),
  P("M340 745 q10 -40 25 -5 q12 -42 28 -2 q14 -36 22 5",.24,.28,{f:C.red,w:8}),
  P(circle(380,790,9),.26,.28,{f:INK,w:6}),
  P("M280 1058 L270 1130 M330 1058 L340 1130 M245 1130 L290 1130 M320 1130 L365 1130",.27,.31,{c:C.orange,w:8}),
  T("لو",950,96,C.gray,.3,.34,{x:540}),
  P("M780 760 C860 760 900 900 900 990 C900 1080 850 1130 780 1130 C710 1130 660 1080 660 990 C660 900 700 760 780 760 Z",.3,.4,{f:"#fff3d6",w:9}),
  T("البيضة!",1350,150,C.green,.4,.5),
  P("M700 700 L720 630 L755 680 L780 615 L805 680 L840 630 L860 700 Z",.48,.54,{f:C.yellow,w:8}),
  T("الديناصورات جانت تبيض",1500,80,INK,.56,.72),
  T("قبل الدجاج بملايين السنين",1615,74,C.blue,.74,.9)]},
 {name:"cta",els:[T("ما عرفت ولا جواب؟",400,104,INK,.0,.15),
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
  for(const sc of SCENES)for(const e of sc.els){if(!e.txt)continue;
    const font=e.font==='cairo'?'ttf/Cairo900.ttf':'ttf/Lalezar.ttf';
    let r=await shape(font,e.txt,e.s);
    if(r.width>960){r=await shape(font,e.txt,e.s*960/r.width)}
    e.width=r.width;e.sc=r.sc;e.glyphs=r.glyphs.map(g=>({d:g.d,x:g.x,y:g.y}));e.x=e.x??540;}
  fs.writeFileSync('scenes.json',JSON.stringify({SCENES,C}));console.log('ok',SCENES.length);
})();
