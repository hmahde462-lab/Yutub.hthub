# Weekly compilations: python3 compile.py  -> videos/hamoudi/compilations/hamoudi-mama-week{N}-parts{a}-{b}.mp4
import json,os,re,subprocess,glob
from PIL import Image,ImageDraw,ImageFont
R="/home/user/yutub.hthub"; V=R+"/videos/hamoudi"; OUT=V+"/compilations"; os.makedirs(OUT,exist_ok=True)
T="/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/compile"; os.makedirs(T,exist_ok=True)
FONT="/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/hm/base/engine/fonts/NotoNaskhArabic-Bold.ttf"
E=json.load(open(R+"/studio/hamoudi-2d/season/season.json"))
GROUPS=[(2,8),(9,15),(16,22),(23,29),(30,36),(37,43),(44,52)]
def sh(c): r=subprocess.run(c,shell=True,capture_output=True,text=True); assert r.returncode==0,(c,r.stderr[-800:]); return r.stdout
def dur(f): return float(sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 '{f}'"))
def epfile(n): return glob.glob(f"{V}/hamoudi-mama-part{n}.mp4")[0] if n>=8 else glob.glob(f"{V}/hamoudi-mama-part{n}-*.mp4")[0]
def cut(n,last):
    f=epfile(n); d=dur(f)
    if last: return f,d
    return f,(16.6 if n==2 else d-2.6+0.15)
def card(w,a,b):
    im=Image.new("RGB",(1080,1920),"#2B1E4A"); dr=ImageDraw.Draw(im)
    for k in range(0,1920,40): dr.line([(0,k),(1080,k+300)],fill="#33245A",width=14)
    f1=ImageFont.truetype(FONT,150); f2=ImageFont.truetype(FONT,84); f3=ImageFont.truetype(FONT,64)
    def c(t,y,f,col): dr.text((540,y),t,font=f,fill=col,anchor="mm",stroke_width=8,stroke_fill="#14121C",direction="rtl",language="ar")
    c("حمودي وماما",760,f1,"#F2C23B"); c(f"تجميعة الأسبوع {w}",960,f2,"#FFFFFF"); c(f"الأجزاء {a} – {b}",1090,f3,"#E8E4FF")
    p=f"{T}/card{w}.png"; im.save(p)
    sh(f"ffmpeg -v error -y -loop 1 -t 1.8 -i {p} -i {R}/studio/hamoudi-2d/brand/overlay.png -f lavfi -t 1.8 -i anullsrc=r=48000:cl=stereo -filter_complex \"[0][1]overlay,fade=in:0:8,format=yuv420p[v]\" -map [v] -map 2 -r 30 -c:v libx264 -crf 18 -c:a aac {T}/card{w}.mp4")
    return f"{T}/card{w}.mp4",1.8
for w,(a,b) in enumerate(GROUPS,1):
    parts=[card(w,a,b)]+[cut(n,n==b) for n in range(a,b+1)]
    ins="".join(f"-t {t:.3f} -i '{f}' " for f,t in parts)
    fc="".join(f"[{i}:v]settb=AVTB,fps=30,format=yuv420p[v{i}];[{i}:a]aresample=48000,afade=t=out:st={max(0,t-0.08):.3f}:d=0.08[a{i}];" for i,(f,t) in enumerate(parts))
    fc+="".join(f"[v{i}][a{i}]" for i in range(len(parts)))+f"concat=n={len(parts)}:v=1:a=1[v][a0];[a0]loudnorm=I=-14:TP=-1.5[a]"
    out=f"{OUT}/hamoudi-mama-week{w}-parts{a}-{b}.mp4"
    sh(f"ffmpeg -v error -y {ins} -filter_complex \"{fc}\" -map [v] -map [a] -c:v libx264 -crf 19 -preset medium -c:a aac -b:a 192k -ar 48000 -movflags +faststart '{out}'")
    print(w,a,b,round(dur(out),1),flush=True)
