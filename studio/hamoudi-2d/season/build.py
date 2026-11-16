# usage: python3 build.py EP [EP...]  -> renders to $OUT/hamoudi-mama-partEP.mp4
import json,os,re,subprocess,sys,shutil
HERE=os.path.dirname(os.path.abspath(__file__))
BASE="/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/hm/base"
WORK="/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/hm/season"
OUT=os.path.join(HERE,"../../../videos/hamoudi")
E=json.load(open(os.path.join(HERE,"season.json")))
def sh(c,**k): return subprocess.run(c,shell=True,capture_output=True,text=True,**k)
def dur(f): return float(sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}").stdout)
def split(wav,d):
    global LINES
    out=sh(f"ffmpeg -i {wav} -af silencedetect=n=-35dB:d=0.18 -f null -").stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
    gaps=[(e-s,s,e) for s,e in zip(st,en) if s>0.3 and e<dur(wav)-0.2]
    if len(gaps)<2: raise SystemExit(f"cannot split {wav}: {gaps}")
    T=dur(wav); L=[len(x[1]) for x in LINES]; tot=sum(L)
    best=None
    for i in range(len(gaps)):
        for j in range(i+1,len(gaps)):
            a,b=gaps[i],gaps[j]; segs=[a[1],b[1]-a[2],T-b[2]]; sp=sum(segs)
            err=sum(abs(sg/sp-l/tot) for sg,l in zip(segs,L))-0.6*(a[0]+b[0])
            if best is None or err<best[0]: best=(err,a,b)
    g=[best[1],best[2]]; cuts=[(0,g[0][1]),(g[0][2],g[1][1]),(g[1][2],T)]
    ds=[]
    for i,(a,b) in enumerate(cuts):
        a=max(0,a-0.04); b=min(T,b+0.06)
        sh(f"ffmpeg -v error -y -i {wav} -ss {a} -to {b} -af silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse -ar 48000 {d}/out/l{i+1}.wav")
        ds.append(round(dur(f"{d}/out/l{i+1}.wav"),3))
    return ds
for ep in sys.argv[1:]:
    D=E[ep]; n=int(ep); d=f"{WORK}/ep{ep}"
    if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(d+"/out")
    for f in ["engine","index.html"]:
        s=f"{BASE}/{f}"; (shutil.copytree if os.path.isdir(s) else shutil.copy)(s,f"{d}/{f}")
    for f in ["film.js","song.js"]: shutil.copy(f"{HERE}/{f}",f"{d}/{f}")
    LINES=D['l']; ds=split(f"{HERE}/voice/e{ep}.wav",d)
    who=["hamoudi" if s=="Hamoudi" else "mama" for s,_ in D["l"]]
    a1=0.8; a2=round(a1+ds[0]+0.55,3); gagt=round(a2+ds[1]+0.45,3); c3=round(gagt+1.4,3); a3=round(c3+0.25,3); end=round(a3+ds[2]+0.85,3); DUR=round(end+2.6,2)
    shots=[{"kind":"wide","who":None,"t0":0.0},{"kind":"close","who":who[1],"t0":round(a2-0.25,3)},{"kind":"gag","who":None,"t0":gagt},{"kind":"close","who":who[2],"t0":c3}]
    vo=[{"at":a,"dur":ds[i],"file":f"out/l{i+1}.wav","who":who[i],"text":D["l"][i][1]} for i,a in enumerate([a1,a2,a3])]
    sc=open(f"{BASE}/../ep7/score.js").read()
    sc=re.sub(r"const EP = 7, TITLE = \"[^\"]*\";",f"const EP = {n}, TITLE = {json.dumps(D['t'],ensure_ascii=False)}, LAST = {'true' if n==52 else 'false'}; const D = {json.dumps(D,ensure_ascii=False)};",sc)
    sc=re.sub(r"const DURATION = [\d.]+;",f"const DURATION = {DUR};",sc)
    sc=re.sub(r"const shots = \[.*?\];\n",f"const shots = {json.dumps(shots)};\n",sc,flags=re.S)
    sc=re.sub(r"const vo = \[.*?\];\n",f"const vo = {json.dumps(vo,ensure_ascii=False)};\n",sc,flags=re.S)
    sc=re.sub(r"const ev = \{.*?\};",f"const ev = {{ gag: {gagt}, end: {end} }};",sc)
    sc=sc.replace("EP, TITLE, shots","EP, TITLE, LAST, D, shots")
    assert "const D =" in sc and "LAST, D" in sc
    open(f"{d}/score.js","w").write(sc)
    for c in ["node song.js","node engine/render.js video","node engine/render.js mux"]:
        r=sh(c,cwd=d)
        if r.returncode: print(ep,c,r.stdout[-500:],r.stderr[-1500:]); raise SystemExit(1)
    os.makedirs(OUT,exist_ok=True)
    slug=f"hamoudi-mama-part{n}"
    shutil.copy(f"{d}/out/ep{ep}.mp4",f"{OUT}/{slug}.mp4")
    print("done",ep,DUR,flush=True)
