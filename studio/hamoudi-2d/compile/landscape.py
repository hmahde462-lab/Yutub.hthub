# vertical compilations -> 16:9 long-form + thumbnails
import json,os,re,subprocess,glob
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R="/home/user/yutub.hthub"; C=R+"/videos/hamoudi/compilations"
T="/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/compile"
W="/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/hm"
FONT=W+"/base/engine/fonts/NotoNaskhArabic-Bold.ttf"
E=json.load(open(R+"/studio/hamoudi-2d/season/season.json"))
GROUPS=[(2,8),(9,15),(16,22),(23,29),(30,36),(37,43),(44,52)]
def sh(c): r=subprocess.run(c,shell=True,capture_output=True,text=True); assert r.returncode==0,(c,r.stderr[-800:]); return r.stdout
def txt(dr,t,xy,size,col,sw=8):
    dr.text(xy,t,font=ImageFont.truetype(FONT,size),fill=col,anchor="mm",stroke_width=sw,stroke_fill="#14121C",direction="rtl",language="ar")
av=Image.open(R+"/studio/hamoudi-2d/brand/avatar.png").convert("RGBA")
def circ(im,s):
    im=im.resize((s,s)); m=Image.new("L",(s*4,s*4),0); ImageDraw.Draw(m).ellipse((0,0,s*4-1,s*4-1),fill=255); return im,m.resize((s,s))
for w,(a,b) in enumerate(GROUPS,1):
    src=f"{C}/hamoudi-mama-week{w}-parts{a}-{b}.mp4"; out=f"{C}/hamoudi-mama-week{w}-parts{a}-{b}-16x9.mp4"
    # side panels
    P=Image.new("RGBA",(1920,1080),(0,0,0,0)); d=ImageDraw.Draw(P)
    txt(d,"حمودي وماما",(330,380),96,"#F2C23B"); txt(d,f"تجميعة الأسبوع {w}",(330,520),64,"#FFFFFF"); txt(d,f"الأجزاء {a} – {b}",(330,630),56,"#E8E4FF")
    a2,m2=circ(av,200); P.paste(a2,(1490,330),m2); txt(d,"@jazar2002",(1590,600),56,"#FFFFFF",6); txt(d,"اشترك وفعّل الجرس",(1590,700),44,"#F2C23B",5)
    P.save(f"{T}/panel{w}.png")
    sh(f"ffmpeg -v error -y -i '{src}' -i {T}/panel{w}.png -filter_complex \"[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.18[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0[m];[m][1]overlay,format=yuv420p[v]\" -map [v] -map 0:a -c:v libx264 -crf 20 -preset medium -c:a copy -movflags +faststart '{out}'")
    # thumbnail: gag frame of a mid episode
    n=a+3 if a+3>=8 else 8
    sc=open(f"{W}/season/ep{n}/score.js").read(); g=float(re.search(r"gag: ([\d.]+)",sc).group(1))
    fr=f"{T}/fr{w}.png"; sh(f"ffmpeg -v error -y -ss {g+0.5} -i '{R}/videos/hamoudi/hamoudi-mama-part{n}.mp4' -frames:v 1 {fr}")
    sc2=f"{T}/fr{w}b.png"; sh(f"ffmpeg -v error -y -ss 2.0 -i '{R}/videos/hamoudi/hamoudi-mama-part{n}.mp4' -frames:v 1 {sc2}")
    th=Image.open(sc2).convert("RGB").crop((0,1050,1080,1050+608)).resize((1280,720)).filter(ImageFilter.GaussianBlur(2))
    gag=Image.open(fr).convert("RGB").crop((140,420,940,1260)).resize((480,504))
    th.paste(gag,(770,140)); dt=ImageDraw.Draw(th)
    dt.rectangle((0,0,1280,720),outline="#F2C23B",width=14)
    txt(dt,"حمودي وماما",(390,190),110,"#F2C23B",10); txt(dt,f"تجميعة الأسبوع {w}",(390,360),80,"#FFFFFF",9); txt(dt,f"{b-a+1} حلقات بفيديو واحد!",(390,500),60,"#FFE7A0",8)
    th.save(f"{C}/thumb-week{w}.jpg",quality=90)
    print("ok",w,flush=True)
