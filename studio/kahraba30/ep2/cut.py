# Split e2c*.mp3 narration chunks into per-scene wavs (line00..53.wav) using silences + proportional prior (DP).
import json,subprocess,re,sys
chunks=json.load(open('ep2_chunks.json')); cuts_all={}
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
for ci,c in enumerate(chunks):
    paras=c['text'].split('\n\n'); n=len(paras); f=f'e2c{ci}.mp3'; D=dur(f)
    out=subprocess.run(['ffmpeg','-i',f,'-af','silencedetect=noise=-38dB:d=0.18','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    gaps=[((s+e)/2,e-s) for s,e in zip(st,en) if s>0.3 and e<D-0.1]
    # speech time estimate per paragraph: chars; total speech = D - sum(gaps used) ~ use D
    L=[len(p) for p in paras]; tot=sum(L); exp=[]; a=0
    for l in L[:-1]: a+=l; exp.append(a/tot*D)
    G=len(gaps); INF=1e9
    # dp[k][g]: best cost placing cut k at gap g
    dp=[[INF]*G for _ in range(n-1)]; bk=[[-1]*G for _ in range(n-1)]
    cost=lambda k,g: abs(gaps[g][0]-exp[k])*1.0 - 6*min(gaps[g][1],1.2)
    for g in range(G): dp[0][g]=cost(0,g)
    for k in range(1,n-1):
        for g in range(G):
            for h in range(g):
                v=dp[k-1][h]+cost(k,g)
                if v<dp[k][g]: dp[k][g]=v; bk[k][g]=h
    g=min(range(G),key=lambda g:dp[n-2][g]); sel=[g]
    for k in range(n-2,0,-1): g=bk[k][g]; sel.append(g)
    sel=sel[::-1]; cuts=[gaps[g][0] for g in sel]; cuts_all[ci]=cuts
    b=[0]+cuts+[D]
    for k in range(n):
        i=c['from']+k
        subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-ss',f'{b[k]:.3f}','-to',f'{b[k+1]:.3f}','-ar','48000','-ac','1',f'../line{i:02d}.wav'],check=True)
    print(ci,[round(x,1) for x in cuts])
json.dump(cuts_all,open('cuts_ep2.json','w'))
