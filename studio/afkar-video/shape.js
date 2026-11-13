// Shape Arabic text with HarfBuzz and return glyph outline paths (in visual order, right-to-left drawing order).
const fs=require('fs');
let hbP=null;
async function hb(){ if(!hbP){ hbP=require('harfbuzzjs').then?require('harfbuzzjs'):Promise.resolve(require('harfbuzzjs')); } return hbP; }
const cache={};
async function shape(fontFile,text,size){
  const h=await hb();
  if(!cache[fontFile]){const blob=h.createBlob(fs.readFileSync(fontFile));const face=h.createFace(blob,0);const font=h.createFont(face);cache[fontFile]={face,font,upem:face.upem};}
  const {font,upem}=cache[fontFile];
  const buf=h.createBuffer();buf.addText(text);buf.guessSegmentProperties();h.shape(font,buf);
  const out=buf.json();buf.destroy();
  const sc=size/upem;let x=0;const glyphs=[];
  for(const g of out){const d=font.glyphToPath(g.g);
    if(d)glyphs.push({d,x:(x+g.dx)*sc,y:-g.dy*sc,cl:g.cl});x+=g.ax;}
  const width=x*sc;
  // transform path: scale, flip y. Done in SVG via transform attribute.
  return {width,sc,glyphs:glyphs.sort((a,b)=>b.x-a.x)};
}
module.exports={shape};
