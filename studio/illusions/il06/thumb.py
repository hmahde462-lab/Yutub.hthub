import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H=1280,720; F='../../flag-battles/fonts/Cairo-ExtraBold.ttf'
im=Image.new('RGB',(W,H),(12,12,18))
p=Image.new('RGB',(640,720),(190,190,190)); d=ImageDraw.Draw(p); cx,cy,R=320,360,230
for i in range(12):
    if i==3: continue
    a=2*math.pi*i/12-math.pi/2; x,y=cx+R*math.cos(a),cy+R*math.sin(a)
    d.ellipse([x-40,y-40,x+40,y+40],fill=(230,110,215))
p=p.filter(ImageFilter.GaussianBlur(14)); d=ImageDraw.Draw(p)
a=2*math.pi*3/12-math.pi/2; x,y=cx+R*math.cos(a),cy+R*math.sin(a)
g=Image.new('RGBA',(640,720),(0,0,0,0)); ImageDraw.Draw(g).ellipse([x-60,y-60,x+60,y+60],fill=(60,255,90,200)); g=g.filter(ImageFilter.GaussianBlur(18))
p=p.convert('RGBA'); p.alpha_composite(g); d=ImageDraw.Draw(p)
d.ellipse([x-38,y-38,x+38,y+38],fill=(70,240,100))
d.line([cx-26,cy,cx+26,cy],fill=0,width=8); d.line([cx,cy-26,cx,cy+26],fill=0,width=8)
im.paste(p.convert('RGB'),(0,0))
d=ImageDraw.Draw(im)
def t(y,s,sz,col,stroke=6):
    f=ImageFont.truetype(F,sz); w=d.textlength(s,font=f,direction='rtl',language='ar')
    d.text((960-w/2,y),s,font=f,fill=col,direction='rtl',language='ar',stroke_width=stroke,stroke_fill=(0,0,0))
t(70,'ركّز 20 ثانية',70,(255,255,255))
t(200,'الوردي',120,(240,110,220))
t(350,'يصير أخضر!',120,(80,240,110))
d.rounded_rectangle([760,560,1160,650],24,fill=(240,60,80)); t(560,'خدعة بصرية 6',56,(255,255,255),0)
# arrow to green dot
d.line([700,330,x+70,y],fill=(255,214,64),width=12); d.polygon([(x+50,y-22),(x+50,y+22),(x+20,y)],fill=(255,214,64))
im.save('thumb.jpg',quality=92)
